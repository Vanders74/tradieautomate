---
title: 'How to Set Up Electrical Award Allowances in Xero Payroll (Without the Manual Math)'
description: 'Xero Payroll does not automatically calculate Electrical Award allowances like height money, tool allowance, and dirt money. Here is the step-by-step setup so your sparkie payroll runs correctly every week.'
pubDate: 'May 19 2026'
category: "Business Growth"
heroImage: '/hero-xero-payroll-electrical.jpg'
tags: ['Xero', 'payroll', 'electrical award', 'electrician', 'payroll setup', 'admin automation']
---

Every Monday morning, the same problem. The bookkeeper opens Xero, looks at the week's timesheets, and starts manually calculating height allowance, tool money, and dirt money for six electricians who all worked different sites with different conditions.

It takes 90 minutes. It creates errors. And it's entirely avoidable.

Here's the thing Xero doesn't advertise: the platform's Standard Payroll tier does not natively calculate the variable allowances under the Electrical Contracting Award 2020. They have to be entered manually — unless you build the right pay items and templates upfront.

This guide shows you exactly how.

---

## Why This Is an Electrical-Specific Problem

The Electrical Contracting Award has some of the most complex allowance structures in Australian industrial awards. Unlike a flat wage rate, electricians are entitled to additional payments based on the specific conditions of each job. The main ones your payroll needs to handle:

**Height Money (Clause 22.2)**
Paid when work is performed 6 metres or more above the ground or floor level. The rate is specific to the height bracket (6–9m, 9m+) and is calculated per hour at those heights.

**Tool Allowance**
A fixed weekly amount paid to electricians who supply and maintain their own tools. Not all employees qualify — it depends on their employment agreement.

**Dirt Money / Refuse Allowance**
Paid when work is performed under conditions that are "unusually dirty." The specific definition matters for compliance, but in practice it covers work in roof cavities, crawl spaces, or contaminated environments.

**Confined Space Allowance**
Additional payment for work performed in certified confined spaces under the Work Health and Safety Act requirements.

These allowances are not optional — they're Award entitlements. Getting them wrong creates underpayment liability. The Fair Work Commission has been active in this space, and electrical contracting has featured prominently in underpayment investigations.

---

## Step 1: Create Custom Pay Items in Xero

In Xero Payroll, allowances are handled as separate pay items attached to each employee's pay run. Start by building the items.

**Navigate to:** Payroll → Payroll Settings → Pay Items → Allowances

Click **Add** to create each of the following:

### Height Allowance (6m+)

- **Name:** Height Allowance — 6m to 9m
- **Type:** Other Allowance
- **Rate:** Current Award rate per hour (check the Fair Work Commission Pay Guide for the Electrical Contracting Award — rate is updated annually)
- **Calculation type:** Fixed amount per unit
- **Units:** Hours
- **PAYG:** Subject to PAYG withholding — Yes
- **Superannuation:** Check your Award interpretation — height allowances are generally *not* subject to super under the SGC definition, but confirm with your accountant

Repeat this process for the 9m+ bracket with the higher Award rate.

### Tool Allowance

- **Name:** Tool Allowance — Weekly
- **Type:** Tool Allowance
- **Rate:** Current Award weekly rate
- **Calculation type:** Fixed amount
- **Units:** N/A (flat weekly rate)
- **PAYG:** No — tool allowances used to purchase/maintain tools are generally exempt from PAYG withholding (confirm with your accountant or ATO)
- **Superannuation:** No — excluded from ordinary time earnings under the SGC

### Dirt Money / Refuse Allowance

- **Name:** Dirt Money — Per Day
- **Type:** Other Allowance
- **Rate:** Current Award daily rate
- **Calculation type:** Fixed amount per unit
- **Units:** Days
- **PAYG:** Yes
- **Superannuation:** Check current position — allowances for special working conditions are generally excluded from OTE

**Important:** Award rates change on July 1 each year following the Annual Wage Review. Set a reminder now to update your pay item rates each July.

---

## Step 2: Build Pay Templates Per Employee Grade

Once your pay items are created, build pay templates for each standard employment grade. The Electrical Contracting Award uses a Grade structure (Grade 1 to Grade 8 for electricians, plus apprentice stages).

**Navigate to:** Payroll → Employees → Select employee → Pay Template

For a **Grade 5 Electrician** (the most common classification for qualified tradespeople with several years of post-trade experience), your template should include:

1. **Ordinary hours** — Award base rate for Grade 5
2. **Tool allowance** — weekly fixed amount (if applicable to this employee)
3. **Height allowance fields** — leave at 0 hours by default; update during pay runs based on site timesheets

Saving this template means the base structure is pre-loaded every pay run. The variable components (height hours, dirt days) are populated from timesheets rather than built from scratch each week.

For apprentices, you'll need separate templates for each year of the apprenticeship (Year 1 through Year 4) because the percentage rates change each year under the Award.

---

## Step 3: Capture the Allowance Data on Site

This is where ServiceM8 and Xero connect — and it's the piece most businesses are missing.

The problem with calculating height allowance manually isn't the formula. It's *knowing* which hours a technician actually spent at height. Unless there's a systematic way to capture this on-site, the bookkeeper is relying on memory, estimates, or incomplete timesheet notes.

ServiceM8's job diary allows technicians to add structured notes and tags to each job as they complete it. By setting up a standard job diary template that includes:

- **Work height field:** "Was height work (6m+) performed? Y/N — if yes, how many hours?"
- **Conditions field:** "Were conditions unusually dirty/confined? Y/N"
- **Completion sign-off:** Technician digital sign-off before leaving the job site

...you create an auditable record of the allowance entitlements for every job, captured at the point of work rather than reconstructed from memory on Monday morning.

The bookkeeper opens the ServiceM8 job record, reads the diary notes, and enters the correct hours into Xero. The calculation is already done. There's no estimation involved.

For a [full walkthrough of ServiceM8 for electrical businesses](/blog/servicem8-for-electricians), including how job diary templates reduce back-office admin by 50–70%, read our detailed review.

---

## Step 4: Run Your First Compliant Pay Run

With pay items created and templates configured, your next pay run works like this:

1. At payroll time, navigate to **Payroll → Pay Runs → New Pay Run**
2. Select the pay period
3. Xero pre-fills each employee's pay from their template
4. Update variable allowances based on job diary data from ServiceM8:
   - Enter height hours for employees who worked at height
   - Enter dirt days for jobs in qualifying conditions
   - Tool allowance is automatic (fixed weekly — already in the template)
5. Review totals, process, and post

What used to take 90 minutes takes 20. What used to require careful manual checking is now template-driven with structured inputs.

---

## Common Mistakes to Avoid

**Conflating tool allowance with expense reimbursement.** Tool allowances are Award entitlements — they're not the same as reimbursing a specific expense. Treating them as expense claims in Xero changes the PAYG and super treatment.

**Not updating rates on July 1.** The Annual Wage Review changes all Award rates. Your Xero pay items won't update automatically — you have to change the rates manually each financial year.

**Ignoring apprentice year transitions.** When an apprentice moves from Year 2 to Year 3, their pay template needs updating. It's easy to miss in a busy business. Put it in your calendar.

**Assuming Xero's superannuation calculation handles allowances correctly.** For non-OTE allowances, Xero's default super calculation may incorrectly include them. Review each pay item's super settings against the current SGC guidelines.

---

## What This Connects To

Payroll compliance is one piece of a larger operational picture for electrical contracting businesses. Related articles that address the broader system:

- [Electrical Contractor Award Rates Australia 2026](/blog/electrical-contractor-award-rates-australia-2026) — full breakdown of current grade rates and entitlements
- [ServiceM8 for Electricians](/blog/servicem8-for-electricians) — how job management software closes the gap between on-site work and back-office admin
- [The Hidden Admin Cost Calculator](/blog/hidden-admin-cost-calculator) — quantify exactly what the manual payroll process is costing your business

---

*This article is general guidance only. Award interpretations can be complex and fact-specific. Consult a qualified payroll specialist or employment lawyer for advice on your specific situation.*

## Related Reading

- [solar compliance checklist](/blog/solar-compliance-checklist-2026)
- [how to get more solar leads in Australia](/blog/how-to-get-more-solar-leads-australia-2026)
- [ServiceM8 review](/blog/servicem8-review-2026)
