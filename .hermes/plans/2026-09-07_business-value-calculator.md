# Tradie Business Value Calculator — Implementation Plan (Layers 1 & 2)

> **For Hermes:** Execute task-by-task. Load `lead-magnet-widgets`, `interactive-lead-magnets`, and `tradieautomate-digital-products` skills before starting.

**Goal:** A free "What's my trade business worth?" calculator that (Layer 1) gives an instant valuation range and captures the email into Brevo, and (Layer 2) upsells a $49–$99 "Full Valuation Report" at 100% margin.

**Architecture:** Standalone Astro page at `/tools/business-value-calculator` (clones the 4 existing calculator pages), self-contained dark-theme widget, Netlify function for email capture into a new Brevo list, email-first delivery of a free PDF summary, and a paid report sold via Payhip/Lemon Squeezy (merchant-of-record).

**Tech Stack:** Astro (`.astro` page) + vanilla JS/CSS in-page + Netlify Function (Node fetch) + Brevo API (contacts + transactional SMTP) + reportlab (free PDF) + Payhip/Lemon Squeezy (paid delivery).

---

## Context — what already exists (do NOT rebuild)

- 4 standalone calculators: `src/pages/tools/{admin-cost-calculator,ev-charger-quote-calculator,solar-quote-calculator,solar-savings-calculator}.astro` — clone one of these for page scaffolding.
- Exit-Readiness Quiz (readiness, NOT valuation): `src/components/ExitReadinessQuiz.astro`, `netlify/functions/exit-readiness-lead.js`, 3 tier PDFs in `public/`. **Cross-link, don't duplicate.**
- Lead-capture function pattern to clone: `netlify/functions/playbook-lead.js`.
- PDF pattern (reportlab, navy/orange, Arial TTF): `scripts/generate-exit-readiness-pdfs-v2.py`.
- Brevo lists currently: 2, 3, 4, 5 (all 0 subs). **List 6 referenced by exit-readiness-lead.js does NOT exist** → quiz leads silently dropped. Must create it OR repoint.

---

## Funnel definition (the actual product)

**Layer 1 — free:**
1. 4-step input: annual revenue → staff size → systems maturity → recurring revenue share.
2. Instant on-screen value RANGE (e.g. "$520K – $780K") — **never gated**, per `lead-magnet-widgets` ("never gate the score").
3. "Email me my valuation summary" → email capture → Brevo list → transactional email delivers the free 1-page "Business Valuation Summary" PDF.

**Layer 2 — paid ($49–$99), 100% margin:**
- "Upgrade: Full Valuation Report" CTA shown after the estimate. The report is a **static deep guide** (not per-user generated — keeps it shippable without a web-generator, which `tradieautomate-digital-products` explicitly parked): valuation methodology, 2026 trade-business multiples, comparable-sale benchmarks, buyer-readiness scorecard, 90-day value-building plan, + a worksheet to drop the user's own numbers in.
- Sold via **Payhip or Lemon Squeezy** (merchant-of-record, handles GST + delivery). Decision recorded below.

---

## Valuation methodology (the domain model — must be defensible + disclaimed)

Small Australian trade businesses sell on **Seller's Discretionary Earnings (SDE) multiple**:

- **SDE ≈ annual revenue × net margin.** Trades run ~12–18% true net margin (systemised businesses at the high end).
- **Multiple** scales with systems maturity + owner-dependence (the software input is the commercial hook — and it's true):

| Systems maturity | Low multiple | High multiple |
|---|---|---|
| Paper / whiteboard, owner-dependent | 1.2× | 1.8× |
| Basic digital (accounting only) | 1.6× | 2.2× |
| Integrated (ServiceM8 / simPRO, staff-led) | 2.0× | 3.0× |

**Formula:** `Value = revenue × margin × multiple`, reported as a range (low × 1.2-ish, high × 3.0-ish). Example: $800K revenue, integrated systems → $96K–$144K SDE → ~$192K–$432K value.

**Non-negotiable caveats (YMYL):** label it "estimate for planning, not a professional valuation"; recommend a licensed business valuer for any transaction; no tax/legal advice. This must appear under the result AND in the PDF.

---

## Payment-rail decision (open question → default)

- **Default:** Payhip or Lemon Squeezy for the paid report. Merchant-of-record: collects/remits GST, hosts the PDF, auto-emails on purchase, ~5% fee. Zero code.
- **Alternative (later):** Stripe Payment Links if volume makes the 5% fee material. Requires self-handling GST + delivery.
- **⚠️ Needs Shane's call** on: (a) which platform, (b) price point ($49 vs $99), (c) whether the report should eventually be personalised (park — needs a web-generator).

---

## Files to create / modify

**Create:**
- `src/pages/tools/business-value-calculator.astro` — page + widget
- `netlify/functions/business-value-lead.js` — lead capture + transactional email
- `scripts/generate-valuation-pdf.py` — free 1-page summary PDF (reportlab)
- `public/business-valuation-summary.pdf` — output
- (paid report PDF delivered by Payhip/Lemon Squeezy — NOT in `public/`; see `tradieautomate-digital-products` storage rule)

**Modify:**
- `src/pages/tools/index.astro` — add the new calculator card
- `src/components/ExitReadinessQuiz.astro` — add cross-link to the calculator (readiness → "$ value")
- `netlify/functions/exit-readiness-lead.js` — fix list-6 bug (create list 6 in Brevo or repoint to an existing list)
- `src/content/blog/sell-servicem8-trade-business-value.md` + `sell-your-solar-business-servicem8.md` — surface the calculator CTA
- `src/content/blog/sparkys-playbook-chapter-12-exit-strategy-valuation-electrical-business.md` — surface the calculator CTA

---

## Step-by-step tasks

### Phase 0 — Brevo list hygiene (do first, unblocks everything)
- [ ] **Task 0.1:** Create Brevo list "Business Value Calculator" via API (`POST /v3/contacts/lists`), record the returned ID.
- [ ] **Task 0.2:** Diagnose list-6 — either create list 6 ("Exit Readiness Quiz") or repoint `exit-readiness-lead.js` to an existing list. Verify the quiz lead path stops dropping contacts.

### Phase 1 — Netlify function (lead capture)
- [ ] **Task 1.1:** Create `netlify/functions/business-value-lead.js` cloning `playbook-lead.js`. Attributes: `FIRSTNAME`, `BV_REVENUE`, `BV_STAFF`, `BV_SYSTEMS`, `BV_RECURRING`, `BV_LOW`, `BV_HIGH` (the estimate), `BV_DATE`. `listIds: [<new list id>]`. Email-first delivery via `POST /v3/smtp/email` from `info@tradieautomate.com`, fallback `downloadUrl` surfaced only on `emailSent === false` (see `lead-magnet-widgets` pattern). Never fail the user on Brevo error.
- [ ] **Task 1.2:** Verify sender `info@tradieautomate.com` is verified in Brevo (Senders & Domains) — this is the #1 silent-failure cause per `lead-magnet-widgets`.

### Phase 2 — Free PDF (Layer 1 deliverable)
- [ ] **Task 2.1:** Create `scripts/generate-valuation-pdf.py` (reportlab, clone `generate-exit-readiness-pdfs-v2.py`): 1-page "Business Valuation Summary" — estimate range, the multiple method in plain terms, 3 next steps, links to 3 articles (full URL, blue underlined), ServiceM8 CTA, disclaimer.
- [ ] **Task 2.2:** Generate to `public/business-valuation-summary.pdf`, verify it opens.

### Phase 3 — The widget + page (Layer 1 core)
- [ ] **Task 3.1:** Create `src/pages/tools/business-value-calculator.astro`. Clone an existing calculator page for header/footer/SEO scaffolding. Widget uses the dark theme (`#0f172a` bg, `#1e293b` cards, `#f97316`→`#ea580c` gradient CTA).
- [ ] **Task 3.2:** Implement the 4-step input → instant range. JS wraps in IIFE, `var` over `let/const`. The valuation formula from the table above, computed client-side. Result shows range + "what drives this" breakdown. **No email gate on the result.**
- [ ] **Task 3.3:** Add the email-capture form (results screen) → POST to `/.netlify/functions/business-value-lead` → success state + Layer-2 upsell CTA ("Upgrade to the Full Valuation Report →" linking to the Payhip/Lemon Squeezy product).
- [ ] **Task 3.4:** ⚠️ **Scoped-CSS pitfall** (`lead-magnet-widgets`): if the widget renders options/results via `innerHTML`, styles must be `<style is:global>` scoped under the unique wrapper ID. Verify no runtime-injected nodes lose styling.

### Phase 4 — Paid report (Layer 2)
- [ ] **Task 4.1:** Write the Full Valuation Report content (static deep guide) — separate from code. Needs Shane's sign-off on price + platform first.
- [ ] **Task 4.2:** Set up the Payhip/Lemon Squeezy product, wire the upsell CTA from Task 3.3 to it.

### Phase 5 — Surface + cross-link
- [ ] **Task 5.1:** Add card to `src/pages/tools/index.astro`.
- [ ] **Task 5.2:** Add cross-links: ExitReadinessQuiz → calculator ("want a dollar figure?"); calculator → quiz ("want to know if you're exit-ready?").
- [ ] **Task 5.3:** Surface the calculator CTA in the two sell-cluster articles + playbook chapter 12.

### Phase 6 — Deploy + verify
- [ ] **Task 6.1:** `npm run build`, commit, push (`main` → Netlify auto-deploy).
- [ ] **Task 6.2:** Verify live: page renders, dark theme intact, result shows without gate, email flow works (test with a throwaway address, then delete the dummy Brevo contact), PDF accessible at `https://tradieautomate.com/business-valuation-summary.pdf`, upsell CTA resolves.

---

## Verification checklist (done = all true)

1. Live page renders with dark theme, no broken styling.
2. 4-step input → instant range, **no email required to see the number**.
3. Email capture writes contact to the new Brevo list with `BV_*` attributes.
4. Transactional email actually arrives (sender verified) — test + confirm, not just "success: true".
5. Free PDF is reachable and opens.
6. Exit-Readiness Quiz no longer writes to a non-existent list.
7. Upsell CTA links to the (configured) paid product.

---

## Risks / open questions

1. **YMYL risk** — valuation is financial-adjacent content. Hard requirement: "estimate only" disclaimer + "get a professional valuation" recommendation everywhere the number appears. Don't overstate precision.
2. **Payment rail + price** — Shane to decide Payhip vs Lemon Squeezy, and $49 vs $99. Do not build Layer 2 delivery until this is settled.
3. **Personalisation deferred** — the paid report is static (recommended for MVP). A per-user generated report needs a web-generator + signed delivery, which is explicitly parked until volume justifies it.
4. **Cannibalisation** — the calculator and the Exit-Readiness Quiz must be positioned as complementary (value vs readiness) with two-way links, not as competing CTAs.
5. **Brevo list-6 bug** — pre-existing; fix in Phase 0 regardless of the calculator.
