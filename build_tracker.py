"""Build the Junk & Move Pros competitor + marketing tracker workbook."""
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

OUT = "/home/hatch/workspace/junkmove-site/Junk-Move-Pros-Competitor-Tracker.xlsx"

wb = openpyxl.Workbook()

HDR_FONT = Font(bold=True, color="FFFFFF", size=11)
HDR_FILL = PatternFill("solid", fgColor="1F4E5F")
SUB_FILL = PatternFill("solid", fgColor="D9E8EC")
THIN = Border(*(Side(style="thin", color="B0B0B0") for _ in ("left", "right", "top", "bottom")))
WRAP = Alignment(wrap_text=True, vertical="top")


def sheet(title, headers, rows, widths):
    ws = wb.create_sheet(title) if title != "Sheet" else wb.active
    if title == "Sheet":
        ws.title = title
    ws.sheet_view.showGridLines = False
    for c, h in enumerate(headers, 1):
        cell = ws.cell(row=1, column=c, value=h)
        cell.font = HDR_FONT
        cell.fill = HDR_FILL
        cell.alignment = Alignment(wrap_text=True, vertical="center")
        cell.border = THIN
    for r, row in enumerate(rows, 2):
        for c, v in enumerate(row, 1):
            cell = ws.cell(row=r, column=c, value=v)
            cell.alignment = WRAP
            cell.border = THIN
            if r % 2 == 0:
                cell.fill = SUB_FILL
    for c, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(c)].width = w
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions
    return ws


# ---- 1. Competitors ----
sheet("Competitors",
      ["Competitor", "Type", "Hudson Valley presence", "Min charge", "1/4 truck", "1/2 truck",
       "Full truck", "Moving rate", "Pricing published?", "Google rating", "Top review weak spots", "Services", "Notes"],
      [
       ["1-800-GOT-JUNK", "Franchise (national)", "No dedicated HV franchise found; nearest Rochester NY / Bronx / Somerset NJ", "~$107 (1/8 truck, advertised)", "unknown", "unknown", "Advertised up to ~$1,099; review-reported $800-$1,800+", "No moving service", "Partial - volume ladder only, no local list", "3.5/5 (allmovers.org)", "1) Quote-to-bill jumps 50-150% on arrival ('bait-and-switch'); 2) sticker shock on small loads ($696 for dresser+grill+boxes); 3) damage claims denied/ignored; 4) pricing opacity", "Full-service junk removal; donation/recycling partners (Goodwill, Habitat ReStore); curbside options", "No HV price list published. Free on-site estimate before work; phone quotes NOT binding."],
       ["College Hunks Hauling Junk & Moving", "Franchise (national)", "Nearest: Mount Kisco (Westchester). None in Orange/Dutchess/Ulster/Putnam/Sullivan/Rockland", "$99 (1/8 truck, online est.)", "unknown", "$459", "$729", "No public hourly rates; 2-3BR NY move est. $1,078-$2,463 (moveBuddha)", "Partial - online broad estimate only", "82.9-88.3% positive (moveBuddha analyses)", "1) Estimates rising sharply on moving day ($550 quoted -> $1,100); 2) property damage + weak claims follow-up ($0.60/lb standard payout); 3) scheduling no-shows; 4) undisclosed surcharges ($80 mattress fee)", "Junk removal + home/office moving + donation pickups + labor services (only national franchise doing both)", "Most directly comparable to Junk & Move Pros (junk + moving). 13 internal price points. Same-day service offered."],
       ["The Junkluggers (Lower Hudson Valley)", "Franchise (regional)", "218 Market St, Clarkstown NY (Rockland County) - physically closest franchise competitor", "$159 (min truckload, ~washer size)", "unknown", "$509", "$759", "n/a (labor services only)", "Partial - national sample pricing; -10% curbside", "4.9/5, 170 reviews (Clarkstown franchise, Google)", "1) High bills for small jobs ($800+ for <1hr job, Thumbtack); 2) on-site price above web quote ($850 web -> $1,100); 3) sloppy ops / no complaint response; 4) thin verified review volume nationally (2.0/5 topconsumerreviews)", "Junk removal, donation pickup, curbside zero-touch pickup, dumpster rental, labor services; eco-friendly branding", "Curbside pickup saves 10%. Phone/online quote may differ from on-site (guaranteed price is on-site). No HV-specific price list."],
       ["LoadUp", "National marketplace", "Operates in Hudson Valley (contractor network)", "$75 single bulky item", "unknown", "unknown", "unknown", "$175/hr labor-only (no truck)", "Yes - instant online pricing", "n/a", "Contractor-marketplace model: not a locally staffed company; quality varies by contractor", "Junk removal from $75; furniture removal from $75 (+$15-30/extra item); moving labor-only", "Claims 20-30% below competition. Ranks #1 for 'mattress removal Hudson Valley' via programmatic town pages."],
       ["Blue Collar", "Local", "Poughkeepsie area (bluecollarext.com)", "$100-$150", "$150-$250", "$250-$400", "$400-$600+", "unknown", "Yes - ranges published", "unknown", "Tells customers to 'always get an upfront quote... to avoid surprises' (implies area competitors don't)", "Junk removal", "Best local junk pricing benchmark found. Single items (couch/mattress) $75-$150 flat."],
       ["Hercules Moving Heroes", "Local", "Catskill NY; serves Catskill/Kingston/Hudson/Greene, NYC->HV relocations", "n/a", "n/a", "n/a", "n/a", "$200/hr (2 movers+truck); $280/hr (3); $350/hr (4); 3-hr min; clock starts at Catskill shop", "Yes - full rate card", "unknown", "Unusually transparent positioning ('No estimate ranges that quietly double on moving day')", "Moving only (no junk removal). NYS DOT MC 43480, USDOT 4551103.", "The transparency model to copy. Market benchmarks: HV movers $180-$220/hr (2 movers+truck), $250-$300/hr (3 movers+truck). Anthony's target: ~$160/hr (20% under $200)."],
       ["Ync Junk Removal", "Local", "67 Sproat St, Middletown NY; 13 yrs in business; (845) 649-3774", "unknown", "unknown", "unknown", "unknown", "unknown", "No", "unknown", "unknown", "Junk removal", "No published pricing found."],
       ["Junk & Move Pros (us)", "Local (owner-operated)", "Ellenville NY -> all Hudson Valley; junkandmove.pro; (845) 402-0555", "TBD - owner sets", "TBD", "TBD", "TBD", "TBD (target ~$160/hr, 20% under Hercules $200/hr)", "Not yet published", "0 (new)", "n/a - set the bar instead: real price before work starts", "Junk removal + moving help + estate/property cleanouts (rare local combo)", "Internal: 50/30/15 markup tiers on cost; gas $4/mi roundtrip; $3,500 cleanout floor. NONE of this publishes."],
      ],
      [30, 20, 34, 16, 14, 14, 30, 30, 22, 20, 48, 30, 40])

# ---- 2. Pricing benchmarks ----
sheet("Pricing Benchmarks",
      ["Service / item", "Franchise range", "Local range", "Our positioning (internal)", "Status", "Source / notes"],
      [
       ["Minimum load", "$99-$159 (franchise min truckload)", "$100-$150 (Blue Collar)", "TBD - between franchises and cheapest locals", "Not published", "competitor-analysis-2026-09-30"],
       ["Half truck", "$459-$509 (franchise sample)", "$250-$400 (Blue Collar)", "TBD", "Not published", "competitor-analysis-2026-09-30"],
       ["Full truck", "$700-$1,800+ (review reality); $729-$1,099 advertised", "$400-$600+ (Blue Collar)", "TBD - target ~$125-$500 across load sizes", "Not published", "competitor-analysis-2026-09-30"],
       ["Single item (couch/mattress)", "$115-$170 (GOT-JUNK est.)", "$75-$150 flat (Blue Collar); $75+ (LoadUp)", "TBD", "Not published", "competitor-analysis-2026-09-30"],
       ["Moving: 2 movers + truck / hr", "n/a (franchises don't publish)", "$180-$220 (HV market); Hercules $200", "Target ~$160/hr (20% below Hercules)", "Not published", "Hercules rate card; Anthony's approved model"],
       ["Moving: 3 movers + truck / hr", "n/a", "$250-$300 (HV market); Hercules $280", "TBD", "Not published", "Hercules rate card"],
       ["Gas / travel", "Baked into opaque pricing", "Baked in", "$4/mile roundtrip (feeds cost basis)", "Internal only", "Anthony's approved model"],
       ["Full house / estate cleanout", "$1,500-$10,000 (Jiffy Junk national); HomeAdvisor avg ~$1,250", "No HV specialist publishes", "$3,500 floor (INTERNAL - never publish)", "Internal only", "youtube-keywords-2026-09-30; Anthony's floor"],
      ],
      [32, 30, 30, 36, 16, 40])

# ---- 3. Keywords ----
sheet("Keywords",
      ["Keyword", "Tier", "Intent", "Competition (est.)", "Target page", "Status", "Notes"],
      [
       ["estate cleanout hudson valley", "1 - attack now", "Transactional", "Low", "/estate-cleanouts-hudson-valley/", "Not started", "VACUUM keyword - flagship money page; matches realtor campaign"],
       ["estate cleanout orange county ny", "1 - attack now", "Transactional", "Low", "/estate-cleanout-orange-county-ny/", "Not started", "Zero mid-HV specialists; SERP pulls Albany/CT"],
       ["estate cleanout dutchess county ny", "1 - attack now", "Transactional", "Low", "/estate-cleanout-dutchess-county-ny/", "Not started", ""],
       ["estate cleanout ulster county ny", "1 - attack now", "Transactional", "Low", "/estate-cleanout-ulster-county-ny/", "Not started", ""],
       ["full house cleanout hudson valley", "1 - attack now", "Transactional", "Low", "/house-cleanout-hudson-valley/", "Not started", "High ticket ($3,500+ internal minimum)"],
       ["hoarding cleanout hudson valley", "1 - attack now", "Transactional", "Low", "/hoarding-cleanout-hudson-valley/", "Not started", "Only Junkluggers lists it generically"],
       ["eviction cleanout poughkeepsie ny", "1 - attack now", "Transactional", "Low", "Town-level service pages", "Not started", "Landlords search this; no local pages"],
       ["eviction cleanout newburgh ny", "1 - attack now", "Transactional", "Low", "Town-level service pages", "Not started", ""],
       ["junk removal ellenville ny", "1 - attack now", "Transactional", "Low", "/junk-removal-ellenville-ny/", "Not started", "Home turf - easiest win; weak one-man sites rank"],
       ["junk removal wurtsboro ny", "1 - attack now", "Transactional", "Low", "/junk-removal-wurtsboro-ny/", "Not started", ""],
       ["junk removal napanoch ny", "1 - attack now", "Transactional", "Low", "/junk-removal-napanoch-ny/", "Not started", ""],
       ["storage unit cleanout kingston ny", "1 - attack now", "Transactional", "Low", "/storage-unit-cleanout-kingston-ny/", "Not started", ""],
       ["shed removal hudson valley", "1 - attack now", "Transactional", "Low", "/shed-removal-hudson-valley/", "Not started", "Common request; almost no dedicated pages"],
       ["hot tub removal hudson valley", "1 - attack now", "Transactional", "Low", "/hot-tub-removal-hudson-valley/", "Not started", "High-ticket single item"],
       ["junk removal poughkeepsie ny", "1 - attack now", "Transactional", "Medium", "/junk-removal-poughkeepsie-ny/", "Not started", "No franchises in local pack - winnable"],
       ["junk removal kingston ny", "1 - attack now", "Transactional", "Medium", "/junk-removal-kingston-ny/", "Not started", ""],
       ["junk removal newburgh ny", "1 - attack now", "Transactional", "Medium", "/junk-removal-newburgh-ny/", "Not started", "LoadUp town page ranks - beat on 'real local crew'"],
       ["junk removal middletown ny", "1 - attack now", "Transactional", "Low-Medium", "/junk-removal-middletown-ny/", "Not started", ""],
       ["mattress removal {town} ny", "2 - town x service", "Transactional", "Medium", "/mattress-removal-{town}-ny/", "Not started", "LoadUp ranks #1 for 'mattress removal Hudson Valley'"],
       ["couch removal {town} ny", "2 - town x service", "Transactional", "Low-Medium", "/couch-removal-{town}-ny/", "Not started", ""],
       ["appliance removal {town} ny", "2 - town x service", "Transactional", "Medium", "/appliance-removal-{town}-ny/", "Not started", ""],
       ["moving help {town} ny", "2 - town x service", "Transactional", "Medium", "/moving-help-{town}-ny/", "Not started", "Publish hourly rate on page"],
       ["movers kingston ny", "2 - town x service", "Transactional", "Medium-High", "/movers-kingston-ny/", "Not started", "Aggregators own it; out-localize with real HV numbers"],
       ["commercial junk removal hudson valley", "2 - town x service", "Transactional (B2B)", "Low-Medium", "/commercial-junk-removal-hudson-valley/", "Not started", "Property managers = campaign audience"],
       ["curbside junk pickup hudson valley", "2 - town x service", "Transactional", "Low-Medium", "/curbside-junk-pickup/", "Not started", "Junkluggers gives 10% curbside discount"],
       ["how much does junk removal cost hudson valley", "3 - informational", "Commercial", "High (Angi)", "/how-much-does-junk-removal-cost-hudson-valley/", "Not published - needs approval", "Trust weapon: addresses #1 customer anxiety (quote inflation)"],
       ["how much do movers cost kingston ny", "3 - informational", "Commercial", "Medium", "Local cost page with HV numbers", "Not published - needs approval", "moveBuddha owns a Kingston cost page"],
       ["dumpster rental vs junk removal", "3 - informational", "Commercial", "Medium", "Blog comparison post", "Not started", ""],
       ["how much does an estate cleanout cost", "3 - informational", "Informational", "Medium", "Cost guide post", "Not published - needs approval", "Realtor/executor audience"],
      ],
      [36, 18, 18, 18, 36, 24, 44])

# ---- 4. Blog calendar ----
sheet("Blog Calendar",
      ["Week", "Topic", "Target keyword(s)", "Angle", "Status"],
      [
       ["5-6", "How Much Does Junk Removal Cost in the Hudson Valley? (2026 Local Price Guide)", "how much does junk removal cost hudson valley", "Real local ranges; volume-ladder table; what drives price", "Draft - needs Anthony's price approval"],
       ["5-6", "Why Do Junk Removal Quotes Change on Arrival? (And How We Price Differently)", "junk removal quote vs final price", "Names the #1 franchise complaint with review evidence; Anthony's counter-promise", "Not started"],
       ["7-8", "How Much Do Movers Cost in Kingston / Newburgh / Poughkeepsie?", "how much do movers cost kingston ny", "Local numbers: $180-$220/hr market, 3-hr minimums, what 'clock starts at the shop' means", "Draft - needs approval"],
       ["7-8", "Dumpster Rental vs. Junk Removal in the Hudson Valley: Which Is Cheaper?", "dumpster rental vs junk removal", "~$300-$500/wk dumpster vs full-service math; when each wins", "Not started"],
       ["9-10", "What Does an Estate Cleanout Cost in the Hudson Valley?", "estate cleanout cost", "Price drivers; donation/consignment offsets; realtor-focused CTA", "Draft - needs approval"],
       ["9-10", "How Much Does Mattress Removal Cost in NY?", "mattress removal cost ny", "$75-$150 range; stairs/box-spring add-ons; county bulk-pickup rules", "Not started"],
       ["11-12", "The Hidden Fees of Franchise Junk Removal (What Reviews Say)", "1-800-got-junk hidden fees", "Review-sourced, factual; mattress surcharges, 'new pricing list' on arrival", "Not started"],
       ["11-12", "The Executor's Checklist: Clearing an Estate in the Hudson Valley", "estate cleanout checklist", "Sort -> donate/consign -> cleanout; realtor/executor audience; ties to email campaign", "Not started"],
       ["Ongoing", "How to Get Rid of a Couch in the Hudson Valley: 5 Options, Ranked", "how to get rid of a couch", "Donate, town bulk pickup, curbside rules, hauler; CTA to couch-removal page", "Not started"],
       ["Ongoing", "How to Dispose of a Mattress in Ulster / Orange / Dutchess County", "mattress disposal ulster county", "County-by-county bulk rules; booked-pickup shortcut", "Not started"],
       ["Ongoing", "What Junk Removal Companies Won't Take (and What to Do Instead)", "hazardous waste disposal hudson valley", "Paint, chemicals, asbestos, tires - county alternatives; builds authority", "Not started"],
       ["Ongoing", "How to Prepare for a Same-Day Junk Pickup", "same day junk removal how it works", "What to stage, access, payment; conversion-focused", "Not started"],
       ["Ongoing", "How to Price a Garage Cleanout Before You Call Anyone", "garage cleanout cost", "Teach cubic-yard math; positions Anthony as the honest teacher", "Not started"],
       ["Ongoing", "Where to Dump It Yourself: Ulster County Transfer Stations & Fees", "ulster county dump fees", "DIY researchers convert when they see the hassle", "Not started"],
       ["Ongoing", "Bulk Pickup Rules by Town: Kingston, Poughkeepsie, Newburgh, Middletown, Ellenville", "{town} bulk pickup schedule", "Hyper-local; each section links to that town's service page", "Not started"],
      ],
      [10, 62, 36, 52, 28])

# ---- 5. Video calendar ----
sheet("Video Calendar",
      ["Week", "#", "Title", "Format", "Status"],
      [
       ["Wk 1", 1, "How Much Does Junk Removal Cost in 2026? (Real Prices, No BS)", "Evergreen explainer", "Not filmed"],
       ["Wk 1", 2, "What 1-800-GOT-JUNK Actually Charges (And Why Local Costs Less)", "Franchise comparison", "Not filmed"],
       ["Wk 2", 3, "How Much Does a Full House Cleanout Cost? (Estate Pricing Explained)", "Evergreen explainer", "Not filmed"],
       ["Wk 2", 4, "How Junk Removal Pricing Works (How Your Quote Is Calculated)", "Hands-only whiteboard", "Not filmed"],
       ["Wk 3", 5, "5 Junk Removal Scams to Avoid (Quote Jumps & Hidden Fees)", "Listicle / voiceover", "Not filmed"],
       ["Wk 3", 6, "What Will Junk Removal Take? (And What They Won't Haul)", "Listicle / voiceover", "Not filmed"],
       ["Wk 4", 7, "How Much Do Movers Cost in 2026? (Hourly Rates Explained)", "Evergreen explainer", "Not filmed"],
       ["Wk 4", 8, "Day in the Life of a Junk Removal Crew (Real Jobs, Real Prices)", "Job vlog", "Not filmed"],
       ["Wk 5", 9, "Hoarder House Cleanout: Before & After (Full Timelapse)", "Before/after timelapse", "Not filmed"],
       ["Wk 5", 10, "How Much Does Junk Removal Cost in the Hudson Valley?", "Local pricing video", "Not filmed"],
       ["Wk 6", 11, "Estate Cleanout in Kingston, NY (Start to Finish)", "Job documentary", "Not filmed"],
       ["Wk 6", 12, "Dumpster Rental vs Junk Removal: Which Is Actually Cheaper?", "Comparison", "Not filmed"],
       ["Wk 7", 13, "Loading a 26ft Box Truck Like Tetris (Moving Day Timelapse)", "POV timelapse", "Not filmed"],
       ["Wk 7", 14, "Full Price Breakdown: Where Your Money Goes on a $X,XXX Job", "Hands-only breakdown", "Not filmed"],
       ["Wk 8", 15, "Eviction Cleanout in Newburgh, NY (What Landlords Should Know)", "Job documentary", "Not filmed"],
       ["Wk 8", 16, "7 Things Your Junk Removal Company Won't Tell You", "Listicle / voiceover", "Not filmed"],
       ["Wk 9", 17, "How Much Does It Cost to Move a 3-Bedroom House in Hudson Valley?", "Local pricing video", "Not filmed"],
       ["Wk 9", 18, "Garage Cleanout Before & After (Poughkeepsie, NY)", "Before/after", "Not filmed"],
       ["Wk 10", 19, "We Get Listings Photo-Ready in 48 Hours (Cleanouts for Realtors)", "Realtor-focused", "Not filmed"],
       ["Wk 10", 20, "Where Does Your Junk Go After We Haul It? (Donate, Recycle, Dump)", "Process / trust", "Not filmed"],
       ["Wk 11", 21, "Office Cleanout in Middletown, NY (Commercial Jobs Explained)", "Job documentary", "Not filmed"],
       ["Wk 11", 22, "Cheapest Ways to Get Rid of Junk (5 Options, Ranked)", "Listicle", "Not filmed"],
       ["Wk 12", 23, "Shed Demolition & Removal (Start to Finish)", "Job documentary", "Not filmed"],
       ["Wk 12", 24, "How to Prepare for Junk Removal Day (Save Money on Your Quote)", "How-to", "Not filmed"],
       ["Wk 13", 25, "Your Junk Removal & Moving Questions Answered (Q&A)", "Q&A", "Not filmed"],
       ["Wk 13", 26, "Why We Started Junk & Move Pros (Our Story - Ellenville, NY)", "Brand story (faceless)", "Not filmed"],
      ],
      [10, 6, 62, 24, 16])

# ---- 6. Viral formats (seeded; updates when competitor-social research lands) ----
sheet("Viral Formats",
      ["Format", "Hook formula (first 3 seconds)", "Example title/caption", "Platform", "Faceless?", "Status", "Notes"],
      [
       ["Before/after reveal", "Show the CLEAN 'after' first, flash back to the mess", "Eviction cleanout in Kingston - 4 hours, one truck", "TikTok/Reels/Shorts", "Yes", "Pending viral research", "Clip 2-3 Shorts per job; zero extra shoot time"],
       ["POV truck-loading timelapse", "Chest-mount camera, 'moving-day Tetris' text overlay", "Loading a 26ft box truck like Tetris", "TikTok/YouTube", "Yes", "Pending viral research", "Own sub-genre (Luke's Moving DFW)"],
       ["Price whiteboard breakdown", "Hands only: 'this load cost $X - here's why'", "Where your money goes on a $X,XXX job", "TikTok/Reels", "Yes", "Pending viral research", "Trust wedge vs franchise quote-jumps"],
       ["Satisfying ASMR cleanup", "Natural sound: tossing, crushing, sweeping", "(no caption needed - let sound carry)", "TikTok/Reels", "Yes", "Pending viral research", "Junk removal is inherently satisfying content"],
       ["Day-in-the-life revenue", "'How much I made today hauling junk' text hook", "Day in the life of a junk removal crew", "YouTube/TikTok", "Yes", "Pending viral research", "JT Junk Solutions format; money angle travels"],
       ["Franchise price comparison", "'[Franchise] quoted $X - here's the real cost'", "What 1-800-GOT-JUNK actually charges", "YouTube", "Yes", "Pending viral research", "Tyler's Hauling owns this as a blog; nobody as local video"],
       ["Hoarder cleanout timelapse", "'Extreme hoarder house - full transformation'", "Hoarder house cleanout: before & after", "YouTube", "Yes", "Pending viral research", "Highest-CPM niche on YouTube (~$33 CPM per vidIQ)"],
       ["Local Loop engagement", "Comment on Valley businesses' posts; tag suppliers", "-", "TikTok", "Yes", "Pending viral research", "Free local SEO no competitor is doing"],
      ],
      [26, 44, 44, 20, 12, 24, 44])

# ---- 7. Update log ----
sheet("Update Log",
      ["Date", "Change", "Changed by", "Notes"],
      [
       ["2026-09-30", "Tracker created from 4 research reports", "Ziggy", "Sources: competitor-analysis, seo-keywords, youtube-keywords, social-playbook (all 2026-09-30)"],
       ["2026-09-30", "Viral Formats tab seeded; full competitor-social research in progress", "Ziggy", "Will update when competitor-social-2026-09-30.md lands"],
      ],
      [14, 52, 16, 52])

# ---- 8. Dashboard / how to use ----
ws0 = wb["Competitors"]
wb.move_sheet("Competitors", offset=-7)  # keep original order
how = wb.create_sheet("READ ME FIRST", 0)
how.sheet_view.showGridLines = False
how["A1"] = "Junk & Move Pros - Competitor & Marketing Tracker"
how["A1"].font = Font(bold=True, size=16, color="1F4E5F")
how["A3"] = "What this is:"
how["A3"].font = Font(bold=True, size=12)
how["A4"] = ("A living workbook built from the 2026-09-30 research sprint. Revisit monthly: check competitors' pricing pages, "
             "Google ratings, and social accounts; update the rows; move Keyword/Blog/Video rows from 'Not started' to 'Live' as work ships.")
how["A4"].alignment = WRAP
how["A6"] = "Tabs:"
how["A6"].font = Font(bold=True, size=12)
tabs = [
    "Competitors - every franchise + local competitor: pricing, review weak spots, services, HV presence.",
    "Pricing Benchmarks - franchise vs local ranges per service; our internal positioning (never publish).",
    "Keywords - Tier 1/2/3 keyword targets with intent, competition, and target pages.",
    "Blog Calendar - 12-week blog plan mapped to keywords.",
    "Video Calendar - 26-video 90-day YouTube plan.",
    "Viral Formats - copyable viral formats + hook formulas (updates when competitor-social research lands).",
    "Update Log - record every change here so the history is visible.",
]
for i, t in enumerate(tabs, 7):
    how.cell(row=i, column=1, value=t).alignment = WRAP
how["A15"] = "Guardrails (standing rules):"
how["A15"].font = Font(bold=True, size=12)
for i, g in enumerate([
    "No published prices without Anthony's approval.",
    'No "licensed & insured" / fleet / crew claims until verified.',
    "Never reveal the internal $3,500 cleanout floor or 50/30/15 markup tiers.",
    "Every row marked 'Not published' stays internal until approved.",
], 16):
    how.cell(row=i, column=1, value="- " + g).alignment = WRAP
for c, w in (("A", 120),):
    how.column_dimensions[c].width = w[1] if isinstance(w, tuple) else w
how.column_dimensions["A"].width = 120
for r in range(4, 20):
    how.row_dimensions[r].height = 30

wb.save(OUT)
print("saved", OUT)
