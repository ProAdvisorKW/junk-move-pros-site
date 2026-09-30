# Junk & Move Pros — junkandmove.pro

Static site. $0/mo stack: Vercel (static hosting) + Supabase (quote form storage).

## Structure
- `index.html`, `junk-removal.html`, `moving-services.html`, `property-services.html`
- `about.html`, `testimonials.html`, `faq.html`, `contact.html`
- `blog.html` + `blog/*.html` (3 migrated posts)
- `videos.html` (placeholder slots — wire embeds when videos arrive)
- `css/style.css`, `js/main.js`, `js/config.js`
- `content/` — raw text pulled from junkandmovepros.com WP API (reference only, not deployed)

## Deploy (Phase 4)
1. Vercel account under junkandmovepros@gmail.com (Hobby, free).
2. New project → import this folder (or push to a new GitHub repo first, then import).
   Framework preset: **Other**. No build command, output dir: `.`
3. Verify on `*.vercel.app`.
4. Supabase project under junkandmovepros@gmail.com → create table `quote_requests`
   (name text, email text, phone text, service text, message text, page text, created_at timestamptz default now()).
   Enable RLS with an INSERT-only policy for anon. Fill `js/config.js` with URL + anon key, redeploy.
5. Raj (Namecheap, junkandmove.pro): add DNS —
   - `A @ 76.76.21.21`
   - `CNAME www cname.vercel-dns.com`
   Then add `junkandmove.pro` + `www.junkandmove.pro` as domains in the Vercel project. SSL auto-provisions.
6. Verify https://junkandmove.pro + https://www.junkandmove.pro.

## Notes
- Phone everywhere: (845) 402-0555 → tel:+18454020555 / sms:+18454020555
- No prices published (awaiting Anthony's pricing-sheet approval).
- Blog launches with 3 migrated posts; publish new ones later.
- Videos page has placeholder slots until Osmo footage arrives.
- Old number (845) 475-8405 and junkandmovepros.com references: none in the build.
