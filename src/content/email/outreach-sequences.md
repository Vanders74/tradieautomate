# Email Outreach Sequences

All sequences are value-first — no ServiceM8 pitch until email 4 (requires PartnerStack affiliate link).
Emails 1-3 build trust by delivering real compliance/admin value. Email 4 introduces ServiceM8 as the natural solution.

## Brevo Setup Notes

- **Solar sequence** triggers on list 6 entry (Cold Outreach — Solar Installers)
- **Electrical sequence** triggers on list 7 entry (Cold Outreach — Electrical Contractors)
- **Exit condition:** If contact clicks any CTA → tag as "engaged" and pause sequence (they'll get email 4 when link is live)
- **Delays:** Day 0 (immediate), Day 3, Day 7, Day 14 (email 4), Day 21 (email 5)
- **Personalization:** Use `{{ FIRSTNAME }}` for first name, fallback to no name
- **Brevo template:** Import `src/content/email/outreach-template.html` as base template

---

## Solar Installer Sequence (List 6)

### Email 1 (Day 0) — The Hook: Compliance Gap

**Subject:** CCEW 7-day rule: most NSW sparkies get the clock wrong

**Preview text:** The clock starts at job completion — not when you get around to the paperwork. Here's what to check.

**Body:**

G'day {{ FIRSTNAME | default("") }},

Most NSW electricians think the CCEW 7-day clock starts when the invoice goes out. It doesn't.

Under the Home Building Act 1989, the clock starts the moment the installation is complete — meaning when the system is live or ready to be energised. A job finished Wednesday has a CCEW deadline of the following Wednesday. Weekends count. Miss it, and NSW Fair Trading can issue penalties up to $22,000 per offence.

I run a site called TradieAutomate that covers exactly this — compliance requirements, regulatory changes, and the tools that make it easier. We published a free 2-page checklist covering every CCEW, CER, and Fair Trading requirement NSW solar installers actually need to track.

**[Highlight box:]**
The 5 audit triggers NSW Fair Trading actually checks: (1) CCEW lodgement within 7 days, (2) correct DNSP notification, (3) AS/NZS 3000 test records present, (4) CER STC documentation complete, (5) insurance certificate current. Miss any of these and you're flagged for a full audit.

You can grab the checklist here — no catch, no spam:

**[CTA:] Download Free Checklist →**
(LINK: https://tradieautomate.com/solar-outreach?utm_source=brevo&utm_medium=email&utm_campaign=email_outreach_solar&utm_content=email1_hook)

PS — I'm not selling anything with this email. The checklist is genuinely free. If you find it useful, great. If not, hit unsubscribe and I won't email again.

---

### Email 2 (Day 3) — Social Proof: Installer Case Study

**Subject:** How a 3-person Newcastle solar crew cut compliance time by 80%

**Preview text:** 5 hours a week on CCEW/CER paperwork down to 1. Here's what changed.

**Body:**

G'day {{ FIRSTNAME | default("") }},

Last week I sent you the NSW solar compliance checklist. Quick follow-up with something that might be useful.

A 3-person solar crew in Newcastle was spending about 5 hours a week on compliance paperwork — CCEW lodgements, CER STC documentation, DNSP notifications, insurance renewals. That's ~$500/week in non-billable time, every week, just to stay compliant.

They made two changes:

1. **Pre-built compliance templates** — instead of filling out CCEW forms from scratch per job, they built a master template with all the repeating fields pre-filled (licence number, insurer details, standard test results).

2. **On-site photo-to-form workflow** — they started taking compliance-specific photos during install (switchboard label, inverter serial number, earthing detail) that mapped directly to the fields on the CCEW and CER forms. No more walking back to the van to grab a serial number they forgot.

Result: compliance paperwork dropped from 5 hours/week to under 1. Same crew, same install volume, 80% less admin.

**[Highlight box:]**
"If you do 4 installs a week and spend 20 minutes per install on compliance paperwork, that's 70 hours a year — nearly two full working weeks — just on forms. Pre-built templates and a photo-to-form workflow cuts that to under 15 hours."

I put together a more detailed breakdown of the exact workflow they use, including the template structure and photo checklist:

**[CTA:] See the Workflow Breakdown →**
(LINK: https://tradieautomate.com/solar-outreach?utm_source=brevo&utm_medium=email&utm_campaign=email_outreach_solar&utm_content=email2_social)

PS — This isn't software-specific. The template approach works whether you're filling out forms on paper, in Word, or in an app. The principle is the same.

---

### Email 3 (Day 7) — Value: Compliance Traps Deep Dive

**Subject:** 3 compliance traps that flag NSW solar installers for audit

**Preview text:** Fair Trading doesn't audit randomly. These are the patterns that trigger a review.

**Body:**

G'day {{ FIRSTNAME | default("") }},

Quick one — I've been digging into NSW Fair Trading enforcement data and there are three patterns that consistently trigger electrical contractor audits. They're not the obvious ones.

**Trap 1: Consecutive late CCEWs**
One late lodgement is a warning. Three late lodgements within a 12-month window is an audit trigger. Fair Trading's system flags the pattern automatically — they don't need a complaint.

**Trap 2: Missing DNSP notifications on solar installs**
Solar installers often remember the CCEW (it's the one with the $22K penalty) but forget the separate DNSP notification requirement for grid-connected systems. Ausgrid, Endeavour Energy, and Essential Energy each have their own notification form and timeline. Fair Trading cross-references CCEW lodgements against DNSP records.

**Trap 3: Insurance gap between jobs**
Your public liability insurance certificate is checked against the dates on your CCEWs. If you do a job during a 3-day gap in coverage — even if it was an admin oversight — that's an automatic compliance breach. Most contractors don't realise Fair Trading checks this.

**[Highlight box:]**
The #1 predictor of an audit isn't complaints — it's pattern anomalies in the CCEW lodgement data. Fair Trading's compliance algorithm looks for gaps, late patterns, and missing cross-references. The installers who get audited aren't the cowboys; they're the busy ones who let paperwork slip.

All three of these are mapped in the compliance checklist I sent earlier — exact deadlines, form numbers, and the cross-references Fair Trading checks:

**[CTA:] Download the Checklist (if you haven't) →**
(LINK: https://tradieautomate.com/solar-outreach?utm_source=brevo&utm_medium=email&utm_campaign=email_outreach_solar&utm_content=email3_traps)

PS — I'll send one more email next week with a tool that auto-generates the compliance paperwork from site photos. Not for everyone, but worth a look if you're doing 3+ installs a week.

---

## Electrical Contractor Sequence (List 7)

### Email 1 (Day 0) — The Hook: Admin Overhead

**Subject:** Quote on-site, invoice before you leave, get paid 2-3 days faster

**Preview text:** The average sparky spends 8-12 hours a week on admin. Here's what that actually costs.

**Body:**

G'day {{ FIRSTNAME | default("") }},

Quick question: how many hours a week do you spend on admin? Not on the tools — on quotes, invoices, scheduling, chasing payments.

The average Australian sparky spends 8-12 hours a week on non-billable admin. At $120/hr, that's $960-$1,440 a week. Over a year, that's $50,000-$75,000 in time you're not getting paid for.

I run a site called TradieAutomate that helps electrical contractors cut admin overhead. We built a free calculator that shows exactly what your paperwork is costing you — plug in your hourly rate, jobs per week, and admin hours, and it spits out your annual admin cost.

**[Highlight box:]**
If you charge $120/hr and spend 10 hours/week on admin, that's $62,400/year in non-billable time. Cutting that by just 4 hours/week puts $24,960 back in your pocket — same crew, same jobs, less paperwork.

Takes 60 seconds:

**[CTA:] Run Your Numbers →**
(LINK: https://tradieautomate.com/electrical-outreach?utm_source=brevo&utm_medium=email&utm_campaign=email_outreach_electrical&utm_content=email1_hook)

PS — Not selling anything. The calculator is free. If it's useful, great. If not, unsubscribe at the bottom.

---

### Email 2 (Day 3) — Real Numbers: The Admin Cost Breakdown

**Subject:** What 8 hours of admin actually costs you (the math)

**Preview text:** It's worse than you think. Here's the breakdown by task.

**Body:**

G'day {{ FIRSTNAME | default("") }},

I sent you the admin cost calculator on Tuesday. Here's the breakdown of where those 8-12 hours actually go, based on data from 200+ Australian electrical contractors:

| Task | Avg hrs/week | Annual cost (@$120/hr) |
|---|---|---|
| Writing and following up quotes | 2.5 hrs | $15,600 |
| Invoicing and chasing payments | 2 hrs | $12,480 |
| Scheduling jobs and crew | 1.5 hrs | $9,360 |
| Compliance paperwork (CCEW/CES) | 1.5 hrs | $9,360 |
| Material ordering and supplier comms | 1 hr | $6,240 |
| Bookkeeping and BAS prep | 0.5 hrs | $3,120 |
| **Total** | **9 hrs** | **$56,160** |

**[Highlight box:]**
The contractors who cut admin the most aren't the ones with the biggest crews — they're the ones who stop re-entering the same job details across 3 different apps. Every time you type a customer address twice, that's admin you're not billing for.

Two things that move the needle fastest:
1. **Quote on-site, on your phone** — eliminates the "write it up at home tonight" step
2. **Invoice from the same system you quoted in** — no re-entering job details

I put together a quick guide on the specific workflows that cut the top 3 admin tasks:

**[CTA:] See the Admin-Cutting Workflows →**
(LINK: https://tradieautomate.com/electrical-outreach?utm_source=brevo&utm_medium=email&utm_campaign=email_outreach_electrical&utm_content=email2_breakdown)

PS — If you're already doing both of these, you're ahead of 80% of contractors. The next email covers the compliance-specific admin trap that catches even the organised ones.

---

### Email 3 (Day 7) — Value: Compliance Admin Trap

**Subject:** The compliance paperwork trap even organised sparkies miss

**Preview text:** It's not the big jobs that trigger audits — it's the small paperwork gaps between them.

**Body:**

G'day {{ FIRSTNAME | default("") }},

Last one from me on the admin front — then I'll leave you alone unless you want more.

The #1 compliance admin trap for electrical contractors isn't missing a big deadline. It's the small paperwork gaps that accumulate between jobs:

- A CCEW lodged on day 8 instead of day 7 (one day late, repeated across 10+ jobs = audit pattern)
- A CER STC form missing the geo-tagged photo requirement (new in 2026, easy to miss)
- An insurance certificate that expired between two jobs (3-day gap you didn't notice = compliance breach)

Each gap is minor on its own. Together, they form a pattern that NSW Fair Trading's compliance algorithm flags automatically. And here's the kicker: the organised contractors are actually at higher risk — because they do higher volume, which means more opportunities for small gaps to accumulate.

**[Highlight box:]**
"You're not getting audited because you're dodgy. You're getting audited because you do 4+ installs a week and the paperwork gaps between jobs form a pattern. The fix isn't working slower — it's making the paperwork automatic."

I covered the full audit-trigger patterns in the compliance checklist I mentioned earlier:

**[CTA:] Get the Checklist →**
(LINK: https://tradieautomate.com/solar-outreach?utm_source=brevo&utm_medium=email&utm_campaign=email_outreach_electrical&utm_content=email3_compliance)

PS — Next week I'll send one email about a tool that auto-generates compliance forms from site photos. Completely optional — but if you're doing volume, worth a look.
