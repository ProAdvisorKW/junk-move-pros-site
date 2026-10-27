# JMP Lead Flow — tasks 120 + 266
**Built:** 2026-10-07 (night batch) · **Status:** code staged, needs Anthony's one-time setup

## Data flow
```
Visitor fills quote form (contact.html, junk-removal.html, ...)
  → js/main.js POSTs to Supabase `quote_requests` (anon key, RLS INSERT-only)
  → tap-to-call / tap-to-text clicks logged to `call_clicks` (best-effort)
  → jmp-twenty-bridge.py (cron, every 5 min):
      polls quote_requests where synced_to_twenty=false
      → creates Person (+ Opportunity, stage NEW) in Twenty via `twenty` CLI
      → marks row synced (only after Twenty confirms)
      → optional instant SMS to Anthony via Twilio (env-gated)
```

## One-time setup (Anthony, ~15 min)
1. Supabase (under junkandmovepros@gmail.com): new project → SQL editor → run `supabase-setup.sql`.
2. Copy the project URL + **anon** key into `js/config.js` (`SUPABASE_URL`, `SUPABASE_ANON_KEY`).
3. Redeploy the static site (Vercel project import, per DEPLOY.md).
4. Bridge env (on whichever machine runs the cron — my VM or AnthonysPad):
   - `JMP_SUPABASE_URL`, `JMP_SUPABASE_SERVICE_KEY` (service_role key)
   - Optional SMS: `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_FROM`, `ANTHONY_MOBILE`
     (note: Twilio A2P brand approval still pending — SMS stays off until then)
5. Cron: `*/5 * * * * /usr/bin/python3 ~/workspace/junkmove-site/jmp-twenty-bridge.py >> ~/workspace/junkmove-site/bridge.log 2>&1`
6. Smoke test: `python3 jmp-twenty-bridge.py --dry-run` (shows pending rows, changes nothing),
   then submit a test quote and watch it land in Twenty.

## What's done vs pending
- DONE: form→Supabase code, tap-to-call logging, RLS SQL, Twenty bridge (Person+Opportunity), SMS hook, config knobs.
- PENDING (Anthony): Supabase project + keys (step 1–2), Twenty topology confirm (task 272 — bridge targets crm.ai-hq.biz via the existing credential; if 'AI - HQ' on AnthonysPad is the live one, point the CLI there), Twilio A2P approval for instant SMS.

## Notes
- No secrets in the repo: keys live in env vars / js/config.js (gitignored on deploy).
- Bridge is idempotent — safe to re-run; failed rows retry next cycle.
- The `twenty` CLI handles Twenty auth via the stored `custom.twenty-crm` credential.
