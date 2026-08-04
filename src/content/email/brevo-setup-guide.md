# Brevo Automation Setup Guide

## Prerequisites

- Brevo account with API key configured in Netlify env vars (`BREVO_API_KEY`)
- Lists 6 (Cold Outreach — Solar Installers) and 7 (Cold Outreach — Electrical Contractors) created
- Contact attributes configured in Brevo (Settings → Contacts → Attributes):
  - `FIRSTNAME` (text)
  - `BUSINESS_NAME` (text)
  - `STATE` (text)
  - `TRADE_TYPE` (text)
  - `SOURCE` (text)
  - `PRIORITY` (number)
  - `SUBURB` (text)
  - `PHONE` (text)
  - `WEBSITE` (text)

## Automation 1: Solar Outreach — Value Sequence (Emails 1-3)

### Step 1: Create Automation
1. Brevo → Automations → Create an automation
2. Name: "Solar Outreach — Value Sequence (Pre-Affiliate)"
3. Entry trigger: "A contact is added to a list" → List 6

### Step 2: Email 1 — "CCEW 7-day rule: most NSW sparkies get the clock wrong"
1. Add action: "Send an email"
2. Timing: Immediately
3. Subject: "CCEW 7-day rule: most NSW sparkies get the clock wrong"
4. Preview text: "The clock starts at job completion — not when you get around to the paperwork. Here's what to check."
5. Import HTML from `src/content/email/outreach-template.html`
6. Paste body content from `src/content/email/outreach-sequences.md` → Solar Email 1
7. CTA link: `https://tradieautomate.com/solar-outreach?utm_source=brevo&utm_medium=email&utm_campaign=email_outreach_solar&utm_content=email1_hook`

### Step 3: Wait + Condition
1. Add action: "Wait" → 3 days
2. Add condition: "If contact has clicked a link in any previous email" → Exit automation, tag as "engaged_solar"

### Step 4: Email 2 — "How a 3-person Newcastle solar crew cut compliance time by 80%"
1. Add action: "Send an email"
2. Subject: "How a 3-person Newcastle solar crew cut compliance time by 80%"
3. Preview text: "5 hours a week on CCEW/CER paperwork down to 1. Here's what changed."
4. Body from `outreach-sequences.md` → Solar Email 2
5. CTA link: `https://tradieautomate.com/solar-outreach?utm_source=brevo&utm_medium=email&utm_campaign=email_outreach_solar&utm_content=email2_social`

### Step 5: Wait + Condition
1. Wait 4 days
2. Same exit condition: "If contact clicked any email" → exit + tag

### Step 6: Email 3 — "3 compliance traps that flag NSW solar installers for audit"
1. Subject: "3 compliance traps that flag NSW solar installers for audit"
2. Preview text: "Fair Trading doesn't audit randomly. These are the patterns that trigger a review."
3. Body from `outreach-sequences.md` → Solar Email 3
4. CTA link: `https://tradieautomate.com/solar-outreach?utm_source=brevo&utm_medium=email&utm_campaign=email_outreach_solar&utm_content=email3_traps`

### Step 7: Wait 7 days (hold for affiliate link)
1. Wait 7 days
2. **PLACEHOLDER:** This is where Email 4 (ServiceM8 pitch) will go when affiliate link is live
3. End of current sequence

---

## Automation 2: Electrical Outreach — Value Sequence (Emails 1-3)

### Step 1: Create Automation
1. Name: "Electrical Outreach — Value Sequence (Pre-Affiliate)"
2. Entry trigger: "A contact is added to a list" → List 7

### Step 2: Email 1 — "Quote on-site, invoice before you leave, get paid 2-3 days faster"
1. Timing: Immediately
2. Subject: "Quote on-site, invoice before you leave, get paid 2-3 days faster"
3. Preview text: "The average sparky spends 8-12 hours a week on admin. Here's what that actually costs."
4. Body from `outreach-sequences.md` → Electrical Email 1
5. CTA link: `https://tradieautomate.com/electrical-outreach?utm_source=brevo&utm_medium=email&utm_campaign=email_outreach_electrical&utm_content=email1_hook`

### Step 3: Wait + Condition
1. Wait 3 days
2. Exit condition: "If contact clicked any email" → exit + tag "engaged_electrical"

### Step 4: Email 2 — "What 8 hours of admin actually costs you (the math)"
1. Subject: "What 8 hours of admin actually costs you (the math)"
2. Preview text: "It's worse than you think. Here's the breakdown by task."
3. CTA link: `https://tradieautomate.com/electrical-outreach?utm_source=brevo&utm_medium=email&utm_campaign=email_outreach_electrical&utm_content=email2_breakdown`

### Step 5: Wait + Condition
1. Wait 4 days
2. Same exit condition

### Step 6: Email 3 — "The compliance paperwork trap even organised sparkies miss"
1. Subject: "The compliance paperwork trap even organised sparkies miss"
2. Preview text: "It's not the big jobs that trigger audits — it's the small paperwork gaps between them."
3. CTA link: `https://tradieautomate.com/solar-outreach?utm_source=brevo&utm_medium=email&utm_campaign=email_outreach_electrical&utm_content=email3_compliance`

### Step 7: Wait 7 days (hold)
1. Placeholder for Email 4 when affiliate link is live

---

## When Affiliate Link Arrives

For each automation, add:

### Email 4 (Day 14) — ServiceM8 Bridge
**Solar subject:** "How ServiceM8 auto-generates CCEW forms from site photos"
**Electrical subject:** "The tool that cuts admin from 10 hrs/week to 3"

Both use the PartnerStack affiliate link with UTM:
```
[PARTNERSTACK_URL]&utm_source=tradieautomate&utm_medium=email&utm_campaign=email_outreach_[solar|electrical]&utm_content=email4_trial
```

### Email 5 (Day 21) — Breakup
Short, no pressure. "If it's not the right time, no worries. Trial still free when you're ready."

---

## Testing Checklist

- [ ] Send test emails to internal address for each sequence
- [ ] Verify: FIRSTNAME personalization works (with and without data)
- [ ] Verify: All links are clickable and resolve correctly
- [ ] Verify: UTM parameters appear in landing page URL
- [ ] Verify: Unsubscribe link works
- [ ] Verify: Exit-on-click condition removes contact from sequence
- [ ] Verify: Mobile rendering (iOS Mail, Gmail, Outlook)
- [ ] Verify: Dark mode rendering
- [ ] Verify: No spam trigger words in subject lines (run through mail-tester.com)
