-- Junk & Move Pros — Supabase setup
-- Run once in the Supabase SQL editor (project under junkandmovepros@gmail.com).
-- Creates quote_requests + call_clicks with INSERT-only RLS for the anon key.

-- ============ quote_requests ============
create table if not exists public.quote_requests (
  id bigint generated always as identity primary key,
  name text,
  email text,
  phone text,
  service text,
  message text,
  page text,
  synced_to_twenty boolean not null default false,
  created_at timestamptz not null default now()
);

alter table public.quote_requests enable row level security;

drop policy if exists "anon insert quote_requests" on public.quote_requests;
create policy "anon insert quote_requests"
  on public.quote_requests for insert
  to anon
  with check (true);

-- The bridge (service_role key) needs to read unsynced rows and mark them synced.
drop policy if exists "service read+update quote_requests" on public.quote_requests;
create policy "service read+update quote_requests"
  on public.quote_requests for all
  to service_role
  using (true)
  with check (true);

-- ============ call_clicks (tap-to-call logging) ============
create table if not exists public.call_clicks (
  id bigint generated always as identity primary key,
  page text,
  link_href text,
  user_agent text,
  created_at timestamptz not null default now()
);

alter table public.call_clicks enable row level security;

drop policy if exists "anon insert call_clicks" on public.call_clicks;
create policy "anon insert call_clicks"
  on public.call_clicks for insert
  to anon
  with check (true);

-- ============ verification ============
-- After running, confirm:
--   select * from public.quote_requests limit 1;
--   select * from public.call_clicks limit 1;
-- Then paste the project URL + anon key into js/config.js and redeploy.
