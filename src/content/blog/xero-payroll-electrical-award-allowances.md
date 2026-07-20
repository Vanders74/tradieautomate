---
title: 'How to Set Up Electrical Award Allowances in Xero Payroll (Without the Manual Math)'
description: 'Xero Payroll does not automatically calculate Electrical Award allowances like height money, tool allowance, and dirt money. Here is the step-by-step setup so your sparkie payroll runs correctly every week.'
pubDate: 'May 19 2026'
updatedDate: 'Jul 19 2026'
category: "Business Growth"
heroImage: '/hero-xero-payroll-electrical.jpg'
tags: ['Xero', 'payroll', 'electrical award', 'electrician', 'payroll setup', 'admin automation']
faq:
  - question: "Does Xero automatically calculate Electrical Award allowances?"
    answer: "No. Xero Payroll does not automatically apply Electrical Award (MA000025) allowances such as height money, tool allowance, or dirt money. Each allowance must be manually configured as a pay item using the correct ATO tax treatment. Once set up, they can be applied per-employee or per-payrun as required."
  - question: "What are the main allowances under the Electrical Contracting Award?"
    answer: "The Electrical Contracting Award (MA000025) includes tool allowance, height allowance (per metre above a set threshold), dirty work allowance, confined space allowance, and travel allowance. Exact rates are updated by the Fair Work Commission annually — check the current award at fairwork.gov.au before setting up Xero pay items."
  - question: "How do I set up tool allowance in Xero for electricians?"
    answer: "In Xero Payroll, create a new Earnings pay item, select 'Allowance' as the type, and set the ATO reporting category to 'Tool allowances' under STP Phase 2 reporting. Enter the current weekly rate from the Electrical Contracting Award (MA000025). Assign the pay item to the relevant employees or add it manually each pay cycle for casual workers."
  - question: "Are Electrical Award allowances subject to superannuation in Australia?"
    answer: "Tool allowances are generally not subject to superannuation under the Superannuation Guarantee (SG) rules — they are reimbursements for expenses, not ordinary time earnings. Other allowances (height, dirty work) may be classified differently. Confirm the correct treatment with your accountant and ensure your Xero payroll setup reflects the correct super calculations."

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

## Dealing With the Annual Rate Update

The Fair Work Commission hands down Annual Wage Review decisions in June each year, with new rates effective from the first full pay period on or after 1 July. For most businesses, this means rates change from early July.

In Xero Payroll, the rate update process is manual:

1. Navigate to **Payroll → Payroll Settings → Pay Items**
2. For each pay item (ordinary hours by grade, each allowance), update the rate to the new Award rate
3. For each employee pay template that uses a fixed wage rate, update the salary/wage amount

This needs to be done before your first July pay run. Set a calendar reminder for late June to check for the Fair Work determination and update your Xero rates.

Failure to update rates from 1 July creates an underpayment situation — one that the Fair Work Ombudsman considers the employer's responsibility to identify and rectify.

---

## Common Mistakes to Avoid

**Conflating tool allowance with expense reimbursement.** Tool allowances are Award entitlements — they're not the same as reimbursing a specific expense. Treating them as expense claims in Xero changes the PAYG and super treatment.

**Not updating rates on July 1.** The Annual Wage Review changes all Award rates. Your Xero pay items won't update automatically — you have to change the rates manually each financial year.

**Ignoring apprentice year transitions.** When an apprentice moves from Year 2 to Year 3, their pay template needs updating. It's easy to miss in a busy business. Put it in your calendar when you hire each apprentice.

**Assuming Xero's superannuation calculation handles allowances correctly.** For non-OTE allowances, Xero's default super calculation may incorrectly include them. Review each pay item's super settings against the current SGC guidelines — or better, have your accountant review the setup.

**Not capturing allowance triggers on-site.** Even with perfect Xero setup, your payroll is only as accurate as the data going in. If technicians don't record which hours were worked at height, the allowance data has to be estimated — which creates both underpayment risk and overpayment risk. Digital capture at the job level is the fix.

---

## When to Bring in a Payroll Specialist

Setting up Electrical Award pay items in Xero isn't complicated if you understand the Award. But there are situations where bringing in a payroll specialist or employment lawyer is the right call:

- You're setting up payroll for the first time with more than 3 employees
- You have employees across different classifications with unusual arrangements
- You want to use an Enterprise Agreement instead of the Award
- You've received a Fair Work inquiry or complaint
- You want to verify that your existing setup is compliant before continuing

A payroll bookkeeper who specialises in trade businesses will typically charge $500–$2,000 to set up and verify Award-compliant payroll in Xero. That's an investment that pays for itself the first time it avoids an underpayment claim.

---

## What This Connects To

Payroll compliance is one piece of a larger operational picture for electrical contracting businesses. Related articles that address the broader system:

- [Electrical Contractor Award Rates Australia 2026](/blog/electrical-contractor-award-rates-australia-2026) — full breakdown of current grade rates and entitlements
- [ServiceM8 for Electricians](/blog/servicem8-for-electricians) — how job management software closes the gap between on-site work and back-office admin
- [The Hidden Admin Cost Calculator](/blog/hidden-admin-cost-calculator) — quantify exactly what the manual payroll process is costing your business
- [Best Accounting Software for Solar & Electrical Businesses](/blog/best-accounting-software-solar-electrical-australia-2026) — Xero vs MYOB vs QuickBooks compared

---

*This article is general guidance only. Award interpretations can be complex and fact-specific. Consult a qualified payroll specialist or employment lawyer for advice on your specific situation.*

---

## FAQ

### Does Xero automatically calculate the Electrical Contracting Award rates?

No. Xero does not natively auto-interpret modern award rates. Xero Payroll allows you to set up pay items for each allowance type, but you must enter the correct rates manually and update them each July following the Annual Wage Review. Xero's automated payroll (Xero Payroll Plus with award interpretation, where available) has broader coverage but should still be verified against the current Award determination for your specific employee classifications.

### Are all Electrical Award allowances subject to superannuation?

No — superannuation applies to ordinary time earnings (OTE), not to all allowances. Tool allowances (used to maintain tools) are generally excluded from OTE and therefore not subject to super. Allowances for uncongenial conditions (height, dirt, confined space) may also be excluded from OTE depending on their nature. This should be confirmed with your accountant based on the current SGC and ATO guidance — the rules can change.

### What's the difference between the Electrical Contracting Award and the Building and Construction Award?

The Electrical, Electronic and Communications Contracting Award 2020 (MA000025) covers electricians, electronic tradespeople, and their apprentices working in installation, maintenance, and service roles. The Building and Construction General On-site Award covers construction workers on building sites. Some electricians working on large construction sites may be covered by the building award instead — which award applies depends on the principal purpose of the work, not just the trade. If your electricians work across both contexts, take advice on which award applies.

### How do I handle overtime in Xero for an electrician?

Overtime rates under the Electrical Award (time and a half for the first 3 hours of overtime, double time after that on weekdays; double time on Sundays; double time and a half on public holidays) must be set up as separate pay items in Xero. Create pay items for each overtime rate category and add them to employee pay runs when applicable. Capturing hours on Xero's built-in timesheets or through your job management system helps ensure overtime is correctly identified and applied.

### Can I use Xero's Auto Superannuation feature with Electrical Award pay items?

Yes — Xero's Auto Superannuation calculates and submits super contributions automatically based on the OTE amounts in each pay run. Once your pay items are correctly configured to include or exclude from OTE as appropriate, the super calculation should be accurate. Review the settings for each allowance pay item to ensure OTE treatment is correctly marked before enabling Auto Super.

---

## Related Reading

- [Solar Compliance Checklist for Australian Installers (2026)](/blog/solar-compliance-checklist-2026)
- [How to Get More Solar Leads in Australia (2026 Guide)](/blog/how-to-get-more-solar-leads-australia-2026)
- [Full ServiceM8 Review 2026: Is It Worth It?](/blog/servicem8-review-2026)
- [EV charger network installation business opportunity](/blog/ev-charger-network-installation-business-opportunity)
- *[Xero vs MYOB for Australian Trade Businesses 2026](/blog/xero-vs-myob-accounting-software-australian-tradies-2026)*
- *[Apprentice Ratios & Hiring Incentives for Electricians Australia 2026](/blog/apprentice-ratios-hiring-incentives-electrical-australia-2026)*
