/* Junk & Move Pros — site config.
   Supabase values wired 2026-10-24: the anon key is a public client key
   (INSERT-only RLS) — safe to ship in the page. Everything else works
   with defaults. */
window.JMP_CONFIG = {
  SUPABASE_URL: "https://xssotlixckhzgkggmngu.supabase.co",
  SUPABASE_ANON_KEY: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inhzc290bGl4Y2toemdrZ2dtbmd1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTA3OTMyODEsImV4cCI6MjEwNjM2OTI4MX0.6tzxraU08cau8DgygunSAAqADKocLcaaTYDPRHmLfVg",
  // Optional fast-path: POST new leads here as well as Supabase.
  // Leave empty to rely on the bridge's Supabase polling (recommended).
  LEAD_WEBHOOK_URL: "",
  BUSINESS_PHONE: "(845) 605-7936",
  BUSINESS_PHONE_TEL: "+18456057936",
  BUSINESS_EMAIL: "junkandmovepros@gmail.com"
};
