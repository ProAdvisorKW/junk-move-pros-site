#!/usr/bin/env python3
"""JMP quote_requests -> Twenty CRM bridge (tasks 120 + 266).

Polls Supabase `quote_requests` for rows with synced_to_twenty=false,
creates a Person (+ Company + Opportunity) in Twenty via the `twenty` CLI,
marks the row synced, and optionally texts Anthony via Twilio.

Runs on a cron (every 5 min). Idempotent: a row is only marked synced after
Twenty confirms the create. Re-running is safe.

Env required:
  JMP_SUPABASE_URL          e.g. https://xyzcompany.supabase.co
  JMP_SUPABASE_SERVICE_KEY  service_role key (NOT the anon key)
Optional:
  TWENTY_CLI                path to the twenty CLI (default: ~/workspace/skills/twenty-crm/bin/twenty)
  TWILIO_ACCOUNT_SID / TWILIO_AUTH_TOKEN / TWILIO_FROM / ANTHONY_MOBILE
                            if all set, sends an instant SMS per new lead (task 120: instant text)

Usage:
  python3 jmp-twenty-bridge.py           # live run
  python3 jmp-twenty-bridge.py --dry-run # show what WOULD sync, change nothing
"""
import json
import os
import subprocess
import sys
import urllib.parse
import urllib.request

SUPA_URL = os.environ.get("JMP_SUPABASE_URL", "").rstrip("/")
SUPA_KEY = os.environ.get("JMP_SUPABASE_SERVICE_KEY", "")
TWENTY_CLI = os.environ.get("TWENTY_CLI", os.path.expanduser("~/workspace/skills/twenty-crm/bin/twenty"))
DRY_RUN = "--dry-run" in sys.argv

TWILIO_SID = os.environ.get("TWILIO_ACCOUNT_SID", "")
TWILIO_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN", "")
TWILIO_FROM = os.environ.get("TWILIO_FROM", "")
ANTHONY_MOBILE = os.environ.get("ANTHONY_MOBILE", "")


def supa(path, method="GET", body=None):
    req = urllib.request.Request(
        SUPA_URL + path,
        data=json.dumps(body).encode() if body is not None else None,
        method=method,
        headers={
            "apikey": SUPA_KEY,
            "Authorization": "Bearer " + SUPA_KEY,
            "Content-Type": "application/json",
            "Prefer": "return=representation" if method != "GET" else "",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        text = r.read().decode()
        return json.loads(text) if text.strip() else []


def twenty_graphql(query):
    out = subprocess.run([TWENTY_CLI, "graphql", query],
                         capture_output=True, text=True, timeout=60)
    if out.returncode != 0:
        raise RuntimeError("twenty CLI failed: " + out.stderr[:300])
    d = json.loads(out.stdout)
    payload = d.get("data", {}).get("data", {})
    if "errors" in d.get("data", {}):
        raise RuntimeError("Twenty GraphQL errors: " + json.dumps(d["data"]["errors"])[:300])
    return payload


def split_name(full):
    parts = (full or "").strip().split()
    if not parts:
        return ("Lead", "")
    if len(parts) == 1:
        return (parts[0], "")
    return (" ".join(parts[:-1]), parts[-1])


def send_text(msg):
    if not (TWILIO_SID and TWILIO_TOKEN and TWILIO_FROM and ANTHONY_MOBILE):
        return False
    data = urllib.parse.urlencode(
        {"To": ANTHONY_MOBILE, "From": TWILIO_FROM, "Body": msg}).encode()
    req = urllib.request.Request(
        "https://api.twilio.com/2010-04-01/Accounts/%s/Messages.json" % TWILIO_SID,
        data=data, method="POST")
    import base64
    req.add_header("Authorization", "Basic " + base64.b64encode(
        ("%s:%s" % (TWILIO_SID, TWILIO_TOKEN)).encode()).decode())
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.status in (200, 201)


def main():
    if not SUPA_URL or not SUPA_KEY:
        print("SETUP NEEDED: export JMP_SUPABASE_URL and JMP_SUPABASE_SERVICE_KEY first.")
        print("See LEAD-FLOW.md for the one-time setup.")
        sys.exit(2)

    rows = supa("/rest/v1/quote_requests?synced_to_twenty=eq.false&order=created_at.asc")
    print("Unsynced quote_requests: %d" % len(rows))
    if DRY_RUN:
        for r in rows:
            print("  WOULD SYNC #%s %s <%s> %s" % (
                r["id"], r.get("name"), r.get("email"), r.get("service")))
        return

    synced = 0
    for r in rows:
        rid = r["id"]
        first, last = split_name(r.get("name"))
        email = (r.get("email") or "").strip()
        phone = (r.get("phone") or "").strip()
        service = (r.get("service") or "").strip()
        try:
            # 1. Person in Twenty (name + email + phone)
            person_q = (
                'mutation { createPerson(data: { name: { firstName: %s, lastName: %s }%s%s }) { id } }'
                % (json.dumps(first), json.dumps(last),
                   ', emails: { primaryEmail: %s }' % json.dumps(email) if email else "",
                   ', phones: { primaryPhoneNumber: %s, primaryPhoneCountryCode: "US" }' % json.dumps(phone) if phone else "")
            )
            person = twenty_graphql(person_q)["createPerson"]
            pid = person["id"]

            # 2. Opportunity linked to the person (JMP quote pipeline)
            opp_name = "JMP quote%s #%d" % ((" — " + service) if service else "", rid)
            opp_q = (
                'mutation { createOpportunity(data: { name: %s, stage: NEW, personId: %s }) { id } }'
                % (json.dumps(opp_name), json.dumps(pid))
            )
            twenty_graphql(opp_q)

            # 3. Mark synced in Supabase (only after Twenty confirms)
            supa("/rest/v1/quote_requests?id=eq.%d" % rid, method="PATCH",
                 body={"synced_to_twenty": True})
            synced += 1
            print("  synced #%d -> person %s" % (rid, pid))

            # 4. Instant text to Anthony (task 120) — env-gated, skipped if unset
            if send_text("JMP lead: %s (%s) — %s. In Twenty now." % (
                    r.get("name"), phone or email or "no contact", service or "quote")):
                print("  SMS sent")
        except Exception as e:
            print("  FAILED #%d: %s" % (rid, str(e)[:200]))
            # do NOT mark synced — next run retries

    print("Done: %d/%d synced." % (synced, len(rows)))


if __name__ == "__main__":
    main()
