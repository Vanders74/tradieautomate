# SERP rank monitor - notes log

Context per keyword check. `keyword_ranks.csv` holds the numbers; this file explains them.
Rotation state: `serp_state.json` (next_index, cycle). Canonical domain: **tradieautomate.com** (Netlify).

## Cycle 1

### 1. how to price solar installations australia - 2026-10-23 - rank >20
- Target page: /blog/how-to-price-solar-installations-australia-2026/ (live, 200, canonical set, indexed).
- Not in top 20 on Bing-backed or Google results. Top 20 is entirely consumer-intent cost content
  (SolarQuotes, Solar Choice, Canstar, hipages, energy.gov.au, EcoFlow, Why Solar, Greenlight).
- Diagnosis: head term is read by Google as a homeowner query. It is not an installer query.
- Proof the page is healthy: for installer-intent phrasing
  "how to price solar jobs as an installer profit margin australia" it ranks **#4**
  (hidden-costs article #3 above it). Both pages are indexed and competing where intent matches.
- Action worth taking: stop chasing the head term; build/cannibalise around installer-intent
  variants ("solar installer profit margin", "how to quote a solar job", "solar quote template")
  where the page already sits page 1. Competitors now in that space: whysolar.com.au (industry
  benchmark pages), flowspec.com.au, solproof.com.au, quotemateapp.au, uprisedigital.com.au.
- Data caveat: Google render was degraded (report said "About 133 results", ~11 organic snippets
  returned), so treat ">20" as "not seen in top 20", not an exact position.

### 2. ev charger installation cost australia - 2026-10-23 - rank >20
- Target page: /blog/ev-charger-installation-cost-australia-2026/ (live 200, canonical correct, title
  "EV Charger Installation Cost Australia 2026: What Electricians Charge and Why", indexed).
- Not in the 20 results returned. Top 20 is pure homeowner cost content: RAA, RACV, RAC WA, Revcharge,
  PumpSwap (owns 3 slots incl. a state cost index), Gridly (2 slots), SolarQuotes, Solar Choice price
  index, zecar, evse.com.au, EV Roadside, quick-quote, goingrate, whatsthedamage, faircost.
- Same pattern as keyword 1: the query is homeowner intent, our page is installer intent. Where the
  intent matches, we rank well — "how much should an electrician charge to install an EV charger
  australia profit margin" returns /blog/ev-charger-installation-electricians-australia-2026/ at #1,
  the network-business guide at #4 and the cost article at #10.
- **New finding - the tool page is invisible.** "ev charger quote calculator electricians australia"
  returns heyjodie.com/en-au/tools/ev-charger-installation-cost-calculator/ at #1 (calculator for
  electricians, installer-facing copy). Our /tools/ev-charger-quote-calculator/ does not appear at all,
  and its H1 is still homeowner-facing: "How Much Does EV Charger Installation Cost in Australia?".
  The URL and body are installer content, the title/H1 are consumer content - it is optimised for a
  query we cannot win and invisible for the one we can.
- Action worth taking: retitle the tool page to installer intent ("EV Charger Quote Calculator for
  Electricians - Price the Job in 30 Seconds"), keep the existing ranges, add a "quote this job" CTA
  into the ServiceM8 trial. That is a title/H1 change, not a rebuild.
- Cannibalisation risk: 7 EV blog pages + 1 EV tool all bidding on overlapping cost/quote terms.
  Only one should own "installation cost" (the cost article); the tool should own "quote calculator"
  and link to the cost article rather than restate its table.
- Competitor note: FlowSpec and thequoteyard.com.au now both publish installer pricing/margin guides,
  and thequoteyard's covers material markup + fixed-price quoting - same territory as our pricing pages.

### 3. best job management software electricians australia - 2026-10-23 - rank 2
- Target page: /blog/best-job-management-software-electricians-australia/ (200, canonical correct,
  title "Best Job Management Software for Electricians Australia 2026", H1 matches, FAQPage + Article
  schema, published 2026-04-14, modified 2026-10-20). First page-1 hit of the cycle.
- Top 20: webblend.au #1, us #2, heyjodie #3, taskrs #4, sprintsuite #5, tradieappfinder #6, fergus.com #7,
  servicescale #8, itrade #9, stackpick #10, capterra (2 slots), tradify, quotemate (2), kynection,
  simpro blog, connecteam, onebookplus.
- **The #1 result is a threat, not a fluke.** webblend.au published their electrician job-management
  page **2026-09-13** (5 weeks old) and took #1 over a page that has been live since April. They are an
  Australian web/automation shop and a **ServiceM8 partner** - direct competitor for the same reader and
  the same affiliate ground. Their page beats ours on framing, not depth:
  - Title: "An Honest Australian Rundown" vs our "Top 5 Platforms Ranked".
  - A **Quick answer** block above the fold (five options, decided by staff count and work type); our
    page has no answer summary - first H2 is "What Electrical Job Management Software Has to Do", and
    the ranking H2 is "Top 5 Platforms Ranked" followed by "ServiceM8 Deep Dive" and "Our Recommendation",
    i.e. it reads as an affiliate listicle to both Google and a reader.
  - Dated price verification inline ("$48/$52/$62 ex GST as checked on their pricing page in August 2026").
    Ours states prices without a checked-on date.
  - Per-page **AI-summary block plus ChatGPT / Claude / Perplexity deep-link CTAs**, i.e. built to be the
    cited source in AI answers, not just a blue link. We have zero of this across the site.
- They also run a wider cluster on our exact audience (simpro price increase 2026, ServiceM8 Office Agent,
  missed call text back, Airtasker for tradies, GoHighLevel for tradies, websites for electricians) plus a
  /wiki/guides/ hub that aggregates the guides for citation. This is a topical-authority build, not
  scattered blog posts.
- Action worth taking (rank-preserving, not a rebuild):
  1. Add a 60-word "Quick answer" block directly under the H1 with the size-based verdict.
  2. Rename "Top 5 Platforms Ranked" to a neutral verdict heading and add the "checked on" date to every price.
  3. Add the AI-summary + LLM-link block pattern from webblend to this page first, then template it.
- Cannibalisation note: our own brand search returns 5 tradieautomate URLs in the top 10 (this page,
  /blog/servicem8-for-electricians/, sparkys-playbook ch8, servicem8-vs-jobber, servicem8-review-2026).
  Split link equity rather than a single strong cluster page - the wiki-hub pattern is the fix, if we build one.

### 4. how to get more solar leads australia - 2026-10-23 - rank 1
- Target page: /blog/how-to-get-more-solar-leads-australia-2026/ (HTTP 200, Netlify edge, canonical correct,
  title/H1 "How to Get More Solar Leads in Australia 2026: $0 vs $250 a Lead", Article + FAQPage schema,
  3,292 words, published 2026-05-16, modified 2026-10-21). **First #1 of the cycle.**
- Top 20: us #1, odindigital.com.au #2, clickclickmedia #3, solarinsights (PDF) #4, growthlocal #5,
  uprisedigital #6, whysolar #7, capitalleads #8, uprisedigital #9, solproof #10, uprisedigital #11,
  leadsnow #12, uprisedigital #13, solproof #14, capitalleads #15, leadshq #16, monstermedia #17,
  click-vision #18, getbatteryquotes #19, localsearch #20.
- Confirms the intent diagnosis from keywords 1-2: we rank >20 on consumer cost queries but #1 where the
  query is installer/business intent. This page's title does the work - a numeric payoff ("$0 vs $250 a
  lead") in the title and meta description. That is the same "answer in the title/snippet" framing that
  webblend used to take #1 on keyword 3. Two data points now; treat it as the house style for blog titles.
- **The win is fragile on the page body.** The title promises a cost comparison and the page contains
  **zero tables** and **zero "checked on"/"as of" dates** on its figures ($80-$250 per lead, $8-$25 per
  click). It opens with ~2 paragraphs of market context before resolving anything. The reader who clicked
  the promise gets prose. whysolar.com.au (#7) publishes a full channel table - cost per lead, close rate,
  time to results, scalability; Odin (#2) ranks "7 Channels Ranked by Effort and Quality". Our ranking is
  currently being carried by title + freshness (updated 2 days ago), not by the body delivering the
  comparison.
- Action worth taking: add a compact 6-row channel comparison block (cost per lead / close rate / time to
  results) under the H1, using figures already in the article, with a "checked Oct 2026" line. Build it as
  stacked cards, not a wide table, so it reads on a phone without horizontal scroll. This is copy plus one
  component, no rebuild.
- **Recurring gap, now confirmed site-wide:** "checked on [date]" price verification is missing here and on
  keyword 3's page. Stop treating it as a per-page fix and add it to the blog template / content checklist.
- Cannibalisation contrast: only **one** tradieautomate URL in this top 20, against five on keyword 3. The
  split-equity problem is local to the job-management cluster, not site-wide. Don't over-generalise the fix.
- Commercial landscape: 6 of 20 slots are lead brokers / bought-lead sellers (capitalleads x2, solproof x2,
  leadsnow, leadshq, getbatteryquotes) and uprisedigital holds 4 slots as an agency cluster. We are #1 over
  agencies and brokers, not over other installers.
- Carried over: EV charger tool page title/H1 swap still open; webblend framing fixes on keyword 3 page still open.

### 5. electrical switchboard upgrade cost australia - 2026-10-23 - rank >20
- Target page: /blog/electrical-switchboard-upgrade-cost-australia-2026/ (live 200 via Netlify edge, canonical
  correct, title/H1 "Electrical Switchboard Upgrade Cost 2026: $1,200–$3,500 by Job Type", Article + FAQPage
  schema, published 2026-07-13, modified 2026-10-20). ~1,990 words, **one table**.
- Not in top 20 on either the exact query or the quoted variant. Confirmed indexed (site: query returns it).
- Top 20: energy.nsw.gov.au #1, electrosurge #2, kongstruction #3, goingrate #4, otterair #5, thequoteyard VIC #6,
  whatsthedamage #7, lckelectrical #8, quotcha guide #9, sparky.fyi #10, thequoteyard SA #11, jentech #12,
  eleco #13, landmark #14, amplus #15, dynamicgroup #16, dlg #17, switchwire #18, sparky.fyi Adelaide #19,
  hipages #20.
- **Intent mismatch, inverted from the EV case.** The title is homeowner ("What Australians pay"), but the body
  opens "the conversation Australian electricians dread most" and the whole article is written to the installer
  (how to quote the conditional allowance, how to script the conversation, how to itemise the invoice). Google
  reads the query as a homeowner price query and serves homeowner cost pages. Same disease as keywords 1–2,
  opposite symptom: there the URL was installer and the H1 consumer; here the H1 is consumer and the body is installer.
- **The winning format is a granular cost table, not a range.** lckelectrical (#8) carries four tables: job-type
  bands with time-on-site, a line-item build-up (enclosure / breakers+RCDs / labour / distributor fee /
  compliance+disposal), a single-vs-three-phase table by amperage, and Reddit invoice corroboration. goingrate (#4)
  runs an interactive state calculator. whatsthedamage (#7) publishes an installed-cost table across job types.
  Our single 5-row table has no per-circuit price, no asbestos line, no distributor fee, no state split — the exact
  columns every page above us publishes.
- **Our price bands are defensible but not quotable.** $1,200–$2,400 basic vs market $900–$2,200 (goingrate),
  $1,200–$1,800 (lck), $1,000–$3,600 (sparky.fyi). The page is not wrong on price; it is under-specified on scope.
  Asbestos removal — a $500–$1,500 line on half the competing pages — appears nowhere in our cost table.
- **Third confirmed page with no "checked on" date.** Now 3 of 5 pages checked this cycle (job management,
  solar leads, switchboard) publish undated prices. This is a template/content-checklist fix, not a per-page one.
- **Programmatic city-page cluster is hogging slots.** quotcha holds 5 of the 20 results in the quoted variant via
  suburb pages (Bilgola Plateau, Wheeler Heights, Fairlight, Beacon Hill, Allambie Heights) that all answer the same
  switchboard-cost question with the same paragraph. That is a doorway pattern worth watching: it can be beaten on
  quality, but it means a single national page will keep losing long-tail real estate to suburb-level pages.
- Cannibalisation: **not** an issue here — ours is the only tradieautomate URL in either top 20. But 18 of our blog
  pages mention switchboards (playbook ch2, RCD page, 3-phase page, EV pages), and none link to this cost page as
  the pricing destination. Fix is internal links, not de-optimisation.
- Action worth taking (highest return first):
  1. Rewrite the opening 80 words for the homeowner who typed the query, then keep the installer sections below an
     explicit "If you're the electrician quoting this job" subhead. Same URL, same title.
  2. Rebuild the single table into three stacked blocks (mobile-first, no wide tables): job-type bands with
     time-on-site; line-item build-up including asbestos and distributor fee; single vs three-phase by amperage.
     All figures already exist in the body or in the linked 3-phase guide — this is re-presentation, not new research.
  3. Add a "checked Oct 2026" line under the cost table and roll the same into the blog template.
  4. Point the RCD, 3-phase and EV pages' switchboard-cost sentences at this page.

### 6. fergus review australia - 2026-10-23 - rank 3
- Target page: /blog/fergus-review-2026-australia/ (200, canonical https://tradieautomate.com/blog/fergus-review-2026-australia/,
  title/H1 "Fergus Review 2026 for Aussie Tradies: $53/User, Pros & Cons", Article + FAQPage + Answer schema,
  published 2026-07-21, modified 2026-10-19, ~2,060 words, 2 tables). **Best position of cycle so far.**
- Position: **#3 on the default search backend**, confirmed by two reads (exact query, then a quoted/variant phrasing
  where it came back #1). Backend read, not a direct Google AU read — Google render is CAPTCHA-blocked from this IP now,
  so treat #3 as "backend", not confirmed Google.
- Same query on other engines is the opposite story: **Bing AU returns 10 results, all fergus.com brand pages** (home, login,
  best-job-management, pricing, help centre) and no tradieautomate. **Brave AU carries us nowhere in its top 20** (capterra,
  softwareadvice, servicescale, fergus.com, trustpilot, ranksvs, tradiespace, g2, thetechyside, officeshed). Third-party
  review coverage on Brave skews to directories, not editorial reviews. Worth one look at why Brave drops us while the
  default backend ranks us 3 — likely backlink/profile, not on-page.
- Top 20 (default backend): servicescale fergus #1, getapp #2, **us #3**, servicescale duplicate #4, backontools #5,
  softwareadvice #6, tripadvisor (Fergus restaurant, Malvern) #7, softwarehq #8, thetechyside #9, capterra #10,
  followupcrm #11, xero app reviews #12, wrenchstack #13, fergus.com/au/industries/builders #14, tradieappfinder #15,
  fergus.com/au/llm-info #16, ranksvs #17, xero app #18, onebookplus #19, capterra directory #20.
- **The dated-price gap is fixed on this page — first one this cycle.** Body reads "Prices verified on fergus.com/au/pricing
  in October 2026", and the page carries a visible "Last updated" line. Of the competitor pages, only softwarehq (8 Sep 2026),
  backontools (18 Aug 2026) and onebookplus (2 Aug 2026) date their prices; servicescale — sitting #1 — stamps "Last verified
  April 2026" against a **$49** entry price that is now wrong by $4 and invents plan names ("Starter"/"Tradie") Fergus does
  not sell. So freshness and accuracy are both on our side at #3. This is the template fix working; carry the pattern to
  the three pages that still fail it (job management, solar leads, switchboard).
- **Why #1 still beats us: servicescale is structured as a verdict, not a review.** Rating block (4.5/5, 180 Capterra reviews),
  "Last verified" trust stamp, "Best for" segmentation by trade, supplier-integration differentiator up top (Reece/Tradelink
  live pricing), and FAQ schema. We have FAQPage schema and a comparison table but no rating/verdict block and no
  "best for / not for" pair above the fold — the H1 drops straight into "What Makes Fergus Different".
- **New competitive signal: fergus.com/au/llm-info/ ranks #16.** The vendor now publishes a page explicitly built for
  generative-AI citation ("Fergus | LLM Info Page for Generative AI"). That is the same AI-summary play webblend used on
  keyword 3, now coming from the vendor itself. Third data point that AI-answer readiness is becoming a ranking surface,
  not just a content nicety.
- **Query ambiguity tax.** Half this SERP is not about job software: a Malvern restaurant (#7), plus musician/Instagram/TikTok
  results for "fergus" on Brave. The head term is contested by unrelated entities, so this position is partly a
  disambiguation win from "australia" + "review", not a pure software-SERP win. Do not over-read a #3 here as strength on
  "fergus review".
- Cannibalisation: only one tradieautomate URL in the top 20 — clean. The separate /blog/servicem8-vs-fergus/ page correctly
  owns the head-to-head intent and this page links out to it. **But the link is one-way**: servicem8-vs-fergus does not link
  back to this review, so the highest-intent comparison page passes no equity to the review. One-line fix.
- Action worth taking (highest return first):
  1. Add the webblend-style **quick verdict block** under the H1: rating out of 5, "best for / not for" in one line each,
     and the $53 vs $77 plan trap — all of it already written further down the page.
  2. Add the reciprocal link from /blog/servicem8-vs-fergus/ (and from /blog/best-job-management-software-electricians-australia/,
     which already links in) into this review.
  3. Keep the October 2026 price date where it is; add the same line to the job-management pillar if it is not there.
  4. Check Brave's blind spot separately — it is a backlink/profile question, not a page-content one.

### 20. electrical contractor award rates australia - 2026-10-23 - rank 5
- Page 1 mid-pack against Fair Work, AwardScale, Valont, VeriTradie, ECA WA. Rate-table snippet holding.

### 7. aroflo review australia - 2026-10-23 - rank >20
- Target page: /blog/aroflo-review-2026-australia/ (HTTP 200, canonical correct, title/H1 "AroFlo Review 2026:
  Honest Pros, Cons & Real Pricing", Article + FAQPage schema, published 2026-07-21, updated 2026-10-20,
  ~2,076 words, 4 data tables). **Indexed and healthy** — `site:tradieautomate.com aroflo` returns it #1.
- Not in the top 20 on the default backend for the exact query, and not in the top 5 on a quoted/variant
  query ("aroflo review" 2026 australian tradies pricing pros cons). Second `>20` miss on a *review* term;
  keyword 6 (fergus) hit #3 with the same page type, so page type is not the variable — see the two
  causes below.
- Top 20 (exact query): Xero App Store reviews #1, servicescale #2, GetApp AU #3, backontools #4,
  aroflo.com/blog #5, aroflo.com/features/job-management #6, tradielink #7, softwareadvice #8,
  thetechyside #9, onebookplus #10, fullstackhvac #11, capterra directory #12, Xero app #13, G2 #14,
  aroflo.com home #15, capterra alternatives #16, tradiespace #17, aroflo.com/request-a-demo-referral #18,
  capterra directory #19, getapp simPRO-vs-AroFlo #20.
- **Cause 1 — the vendor owns the SERP.** FIVE of the 20 slots are aroflo.com (blog, features, home,
  demo-referral, and a review-strewn feature page), plus review-count snippets on three of them
  ("4.4 / 5 (112 reviews)"). Compare keyword 6: fergus.com held two slots. AroFlo also runs its own
  "8 Best Construction Estimating Software" comparison post — the vendor publishing listicles. Review
  intent here is being absorbed by the brand plus four directories (Xero, GetApp, Capterra x3,
  Software Advice, G2). That leaves roughly 4 editorial slots, and backontools, servicescale,
  thetechyside and tradielink have them.
- **Cause 2 — our own two pages contradict each other on AroFlo's pricing, and this page contradicts itself.**
  This review says "AroFlo doesn't publish pricing — a quote is required" and then estimates
  $80–$150/user/month, while its own <title>, meta description and tags promise "$80 ... **Real Pricing**".
  Meanwhile /blog/servicem8-vs-aroflo/ states "$80 per user/month" as **the published rate with a three-user
  minimum**, plus a $1,450 Smart Start. Two pages, two pricing models for the same vendor, both linked to
  each other. That is the single worst trust signal on the cluster and it is cheap to fix.
- **The $80 figure itself is the market's top estimate, not the market's number.** Independently observed
  across this SERP: Capterra and GetApp both list "from A$39/user/month"; arrivy repeats Capterra's $39;
  servicescale publishes $65 field / $75 office; tradiescaler $65; besttradiesoftware $235/mo for three users
  (≈$78/user); fullstackhvac "starting A$39". webblend (the #1 on keyword 3) states AroFlo **withdrew**
  published pricing and that its last self-published figures were **$67/user with a $335 monthly minimum**,
  onboarding from $2,900. So: $39 low, $65–$78 mid, $80 high, $150 (our FAQ upper bound) unsupported by
  anything on this SERP. Our range is defensible at the top end and wrong at the bottom.
- Third-party ratings conflict too, and the number in our snippets is a decade of drift: Capterra 4.3–4.4
  (112–118 reviews), GetApp 4.3 (118), G2 3.5 (**1** review), Xero App Store 3.9 (17). Our page quotes none
  of them, which is why servicescale (#2) gets the click with a rating block.
- **No dated price line and no rating block** — the two gaps already flagged on keywords 3, 4 and 5. This is
  page four of seven checked this cycle with undated prices. It is now unambiguously a template fix.
- Cannibalisation: two tradieautomate URLs compete for AroFlo terms (this review and servicem8-vs-aroflo),
  and on the variant query servicem8-vs-aroflo outranks this page — the comparison page is the stronger
  asset. Reciprocal links exist in both directions here, so this is **not** the keyword-6 one-way-link
  problem.
- Action worth taking (highest return first):
  1. Reconcile the pricing claim across the two pages, pick one model, and date it ("AroFlo withdrew
     published pricing; last self-published rate $67/user, $335/mo minimum — checked Oct 2026"). One hour,
     fixes a self-contradiction and the freshness gap at once.
  2. Add a rating/verdict block under the H1 (4.3/5 across Capterra 118 + GetApp 118, best-for/not-for,
     the $240 three-user floor). Copy already exists in "Who Should Use AroFlo" and "The Verdict".
  3. Stop bidding the head term alone — the vendor + four directories own it. Either target
     "aroflo alternative for electricians" / "aroflo vs servicem8 for electricians" where we already rank,
     or accept page-2 here and push equity to servicem8-vs-aroflo.
  4. Fix the meta description so it does not promise pricing the body says does not exist.

### keyword 8 — "servicem8 alternative for electricians" — >20 (2026-10-23)
- Exact query: **not in the top 20**. Third consecutive miss of the cycle, but the first one whose cause is
  not on-page — **there is no page targeting this keyword, and no alternatives hub anywhere on the site.**
- Top 20 (exact query): tolodora "7 Best Invoicing Software for Electricians" #1, fieldcamp #2, heyjodie (UK)
  #3, mycontractortools #4, servicepro #5, servicetitan blog #6, dashlink (UK) #7, beltstack #8, gitnux #9,
  fieldcamp (mirror) #10, gitnux #11, onebookplus #12, webblend #13, fieldcamp #14, topalternatives #15,
  tradiescaler #16, spotsaas #17, servicetitan/fergus-alternatives #18, althunt #19, checker.app (UK) #20.
  Zero tradieautomate URLs. Note how many slots are low-quality aggregators (fieldcamp ×3, gitnux ×2) — this
  is a soft SERP, not a vendor- or directory-locked one like aroflo.
- Variant check "servicem8 alternatives australia": **also absent, 20/20.** Capterra #1, onebookplus #2,
  itrade #3, tradiescaler #4, fieldcamp #5, tradieappfinder #6, softwarehq #7, askhayley #8, leadduo #9,
  clevero #10, opsler #11, quotemate #12, itrade #13, taskr #14, **fergus.com/au/servicem8-vs-fergus #15**,
  itrade #16, cleverops #17, sprintsuite #18, leadduo #19, fervorstudio #20.
- **The structural gap: 125 posts, seven head-to-heads (Tradify, simPRO ×3, AroFlo, Fergus, Jobber), and no
  hub.** Every comparison we own is a spoke with no parent. The alternatives SERP is a hub query — the intent
  is "what else is there", which we answer only as a `## How ServiceM8 Compares to the Alternatives` H2
  buried 203 lines into /blog/servicem8-for-electricians/ (live 200, 4,264 words). An H2 cannot win a title
  match against ten pages whose H1 is literally "ServiceM8 alternatives".
- **Secondary finding — the SERP is entirely vendor-captured.** onebookplus (.com.au and .com), itrade, taskr,
  quotemate, cleverops, askhayley, sprintsuite, opsler, jobbit are all competitors publishing "alternatives"
  pages that rank their own product first. Add fergus.com's AU page and Capterra. So the honest-neutral slot
  is empty; that is the opening, and it is the one thing an affiliate is well-placed to occupy — with the
  disclosure that already exists on the electricians page.
- **One strategic caveat, stated plainly:** we are a ServiceM8 affiliate ($500 + up to 20% recurring). An
  alternatives page sends traffic to the decision moment, not away from the product; the honest framing
  ("here is who should leave ServiceM8, here is who should not") is both the ranking play and the conversion
  play. If the positioning can't tolerate that, the alternative is to leave the keyword to competitors and
  stop tracking it — but then remove it from the queue rather than re-checking it every cycle at >20.
- **Pricing data is our strongest asset on this SERP — and it is corroborated, unlike the AroFlo cluster.**
  truespeak (#5 on the variant) publishes ServiceM8 AUD incl GST exactly as our table does — $0 / $29 / $79 /
  $149 / $349, unlimited users, job caps — and Tradify at $48 / $52 / $62 ex GST. Everyone else is stale or
  currency-mixed: fieldcamp "~$29/mo USD", mycontractortools "Free–$349", itrade "£29", fervorstudio "$24
  Jobber". Our table (Free/Starter/Growing/Premium/Premium Plus, SMS allowances, card rates) is the most
  complete on the SERP. That is the differentiator to lead with — not a rewritten listicle.
- Also note: ServiceM8 itself has **no page** on this SERP. fergus.com does (`/au/servicem8-vs-fergus/`, #15).
  The brand we're paid to promote is out-flanked on "its" own alternatives query by its competitor's
  comparison page. That is an argument the affiliate manager will care about.
- Action worth taking (highest return first):
  1. **Build /blog/servicem8-alternatives-australia/** as the hub: table of Tradify, Fergus, AroFlo, simPRO,
     Jobber, Ascora by size/device/price with a "checked Oct 2026" stamp; then route every one of the seven
     existing head-to-heads into it as the deeper read. This also fixes the orphaned-spoke problem.
  2. Re-aim the electricians page's H2 into a short "alternatives" block with an anchor and a link to the hub,
     and add "alternatives" to its title/meta only if the hub doesn't cannibalise it.
  3. **Resolve the duplicate matchups before adding more pages.** We have servicem8-vs-simpro-comparison-
     australia **and** servicem8-vs-simpro-electricians-australia-2026; servicem8-vs-tradify-comparison-
     australia **and** servicem8-vs-tradify-solar-electrical; simpro-vs-servicem8-hvac-small-business as a
     third simPRO page. Same cannibalisation the aroflo finding flagged, now measured across the cluster.
  4. Add a visible "Prices checked October 2026" line above the pricing table — the page has `updatedDate:
     Oct 20 2026` but no in-body date, which is the same template gap already logged on keywords 3–7.

## Queue integrity note (2026-10-23)
- `keyword_queue.txt` now holds **18** keywords; the ccew keyword processed last run is no longer in it, so the
  file shifted by one under the saved `next_index`. This run was pinned to the announced keyword
  (electrical switchboard upgrade cost), which now sits at file index 5, and `next_index` was left at 6 so
  **fergus review australia** is next. If keywords get added/removed again, reconcile against `last_keyword`
  before trusting the index or a run will silently skip one.

## Domain note (2026-10-23)
- tradieautomate.com.au resolves to 103.42.108.46 and serves a parked "Your Domains" page over
  HTTP; HTTPS fails the TLS handshake entirely. It is not the live site and is not referenced
  anywhere in the repo. Only a problem if anything external links or cites the .com.au spelling,
  or if you intended to own it. Worth checking the registrar.

## Keyword 09 — "ai automation for tradies" (2026-10-23, cycle 1)
- **Rank: >20. Absent from the top 20 on both queries.** Exact query: 20/20 no tradieautomate URLs.
  Variant "ai automation tradies australia": also 20/20 absent. Backups: `keyword_ranks.csv.bak-20261023-kw09-aiauto`.
- **This is NOT a coverage miss — we have four AI pages.** Unlike the servicem8-alternatives run (no page at all),
  this keyword has 4 dedicated posts, ~10.5k words total, all live 200:
  - ai-business-assistants-tradies — 2,616 w, updated Jul 30
  - ai-automation-trade-business-australia — 3,014 w, updated Oct 1  ← de facto hub
  - ai-automation-electrical-plumbing — 2,594 w, updated Sep 16
  - ai-automation-solar-installers — 2,334 w, updated Sep 16
  Plus email-automation-for-tradies-2026 (3,350 w) as an adjacent piece. Diagnosis is title-match +
  intent mismatch, not thin content.
- **Title match: zero.** No page carries "AI automation for tradies" in title or H1. Closest:
  "AI Automation for Electricians and Plumbers" (audience-restricted) and "Tradie Automation: Use AI to Run
  Your Business on Autopilot" (word order reversed, no "AI automation" adjacency).
- **Internal link structure is inverted.** ai-automation-trade-business-australia has **37 inbound** internal
  links — it is already the hub, but its title doesn't say so. ai-business-assistants-tradies has **0 inbound**
  internal links — it is fully orphaned despite being the newest (May 2026) and most differentiated piece.
  ai-automation-electrical-plumbing: 2 inbound. ai-automation-solar-installers: 10 inbound. So the fix is
  retitle-and-connect, not build-a-new-hub.
- **SERP composition — commercial service intent, not software research.** Exact query top 20:
  tradiehub.net/automation #1, ai.loudachris #2, servicescale blog #3, yesaiautomation #4, theaiimpact #5,
  made4tradies #6, servicescale #7, sophie.com.au #8, workvolve #9, servicescale #10, aivy #11, aitrades #12,
  synergai #13, freetide.ai #14, systree #15, octavius.ai #16, loudachris blog #17, proanalytica #18,
  yesai.au #19, dossisdigital #20. Roughly 14 agencies selling managed automation, 4 editorial blogs,
  2-3 product vendors. Repeat domains: servicescale ×3, loudachris ×2.
  Variant "ai automation tradies australia": aitrades #1, tradie-ai.com.au #2, ai-tradies.au #3,
  ai-automation.au #4, systree #5, made4tradies #6, servicescale #7, aitrades/about #8, linkedin/leadblokes #9,
  linkedin/tradie-ai #10, made4tradies #11, ai-tradies.au #12, onautopilot #13, vibe0 #14, systree #15,
  dynamicdigitalsolutions #16, 13labs #17, melbourneaiagents #18, aivy #19, orvxai #20.
- **Striking absence: no job-management vendor on the board.** ServiceM8, Tradify, simPRO, Fergus, AroFlo — none
  rank. Capterra/software directories — none rank. Even "AI tools" queries usually pull a directory; this one
  doesn't. The two product pages that do rank (sophie.com.au #8, freetide.ai #14) are AI *add-on* tools, not
  job platforms. That is the gap we can actually occupy: "AI automation layered on the job software you already
  run" — our exact ServiceM8 + Sophiie AI framing.
- **Editorial slots exist and are soft.** servicescale holds three slots with blog posts and is itself a
  marketing agency — proof that an agency-adjacent blog can rank here. aivy #11 is a review-style piece.
  So ~4 of 20 slots are genuinely editorial, and they're the ones a content site can win.
- **Honest caveat.** Searcher intent here leans "who can do this for me", and we sell software recommendations,
  not managed services. An editorial piece can capture the research subset, but this will never be a
  high-conversion keyword for an affiliate — expect traffic and email capture, not ServiceM8 trials.
- Action order:
  1. **Retitle the existing hub** — ai-automation-trade-business-australia → "AI Automation for Tradies: What
     Actually Works in 2026 (Australia)". It already has 37 inbound links and the most depth. No new page needed.
  2. **Un-orphan ai-business-assistants-tradies** — add it to the hub as the voice-AI/receptionist spoke and
     link it from the hub plus 3-4 other AI-adjacent posts. Zero inbound links is a straight waste.
  3. **Decide the vertical split.** Electrical/plumbing (2 inbound) and solar (10 inbound) should read as
     spokes under the hub, not peers. Cross-links exist; the anchor text needs to say "AI automation for
     tradies" on at least the hub-to-spoke and spoke-to-hub pairs.
  4. **Add a "checked October 2026" stamp and a DIY-vs-done-for-you comparison table** to the hub. Every
     ranking page on this SERP is either an agency pitch or a tool list; none prices the options against each
     other. Our existing AUD pricing tables give us that in one edit.
  5. Do NOT create a fifth AI page. Four pages with no head term is already the problem.
- Next keyword: **"nsw electrical contractor licence guide"** (state advanced 9→10, cycle 1).
