# UTM Tracking & GA4 Attribution for Email Outreach

## UTM Campaign Structure

Every email link carries full UTM parameters for GA4 attribution.

### Campaign Matrix

| Segment | utm_source | utm_medium | utm_campaign | utm_content |
|---|---|---|---|---|
| Solar Email 1 | brevo | email | email_outreach_solar | email1_hook |
| Solar Email 2 | brevo | email | email_outreach_solar | email2_social |
| Solar Email 3 | brevo | email | email_outreach_solar | email3_traps |
| Solar Email 4 (future) | brevo | email | email_outreach_solar | email4_trial |
| Solar Email 5 (future) | brevo | email | email_outreach_solar | email5_breakup |
| Electrical Email 1 | brevo | email | email_outreach_electrical | email1_hook |
| Electrical Email 2 | brevo | email | email_outreach_electrical | email2_breakdown |
| Electrical Email 3 | brevo | email | email_outreach_electrical | email3_compliance |
| Electrical Email 4 (future) | brevo | email | email_outreach_electrical | email4_trial |
| Electrical Email 5 (future) | brevo | email | email_outreach_electrical | email5_breakup |

### Affiliate Link Pattern

All ServiceM8 trial links carry:
```
?ref=tradieautomate&utm_source=tradieautomate&utm_medium=email&utm_campaign=email_outreach_[segment]&utm_content=email[N]_[type]
```

### Landing Page Links

```
Solar checklist:   https://tradieautomate.com/solar-outreach?utm_source=brevo&utm_medium=email&utm_campaign=email_outreach_solar&utm_content=email[N]_[type]
Electrical calc:   https://tradieautomate.com/electrical-outreach?utm_source=brevo&utm_medium=email&utm_campaign=email_outreach_electrical&utm_content=email[N]_[type]
```

---

## GA4 Events

### Email Click Event

Fire on landing page load when UTM source = 'brevo':

```javascript
// In landing page <script> — auto-fires on page load from email
(function() {
  const params = new URLSearchParams(window.location.search);
  if (params.get('utm_source') === 'brevo' && params.get('utm_medium') === 'email') {
    if (typeof gtag !== 'undefined') {
      gtag('event', 'email_click', {
        event_category: 'email_outreach',
        event_label: params.get('utm_campaign') || 'unknown',
        campaign: params.get('utm_campaign') || 'unknown',
        content: params.get('utm_content') || 'unknown',
      });
    }
  }
})();
```

### Lead Magnet Download Event

Already implemented in landing pages. Fires on successful form submission:
- Event: `lead_magnet_download`
- Campaign: `email_outreach_solar` or `email_outreach_electrical`

### Affiliate Click Event (when PartnerStack link live)

Fire on CTA click to ServiceM8:
- Event: `affiliate_click`
- Campaign: `email_outreach_solar` or `email_outreach_electrical`

---

## GA4 Admin Setup

In GA4 Admin → Events → Conversions:
1. Mark `email_click` as conversion
2. Mark `lead_magnet_download` as conversion (may already be set)
3. Create Explorations report: "Email Outreach Funnel"
   - Step 1: email_click (landing page visit)
   - Step 2: lead_magnet_download (checklist/calculator download)
   - Step 3: affiliate_click (ServiceM8 trial click)

---

## Dashboard Integration

Add to `scripts/dashboard_generator.py` under engagement/conversions:

```python
# Email outreach campaign metrics
def pull_email_outreach_stats():
    """Pull GA4 conversion data for email outreach campaigns."""
    campaigns = ['email_outreach_solar', 'email_outreach_electrical']
    stats = {}
    for campaign in campaigns:
        stats[campaign] = {
            'email_clicks': pull_ga4_events('email_click', campaign=campaign),
            'downloads': pull_ga4_events('lead_magnet_download', campaign=campaign),
            'affiliate_clicks': pull_ga4_events('affiliate_click', campaign=campaign),
        }
    return stats
```

Dashboard card:
```
📧 Email Outreach
| Campaign       | Clicks | Downloads | Trial Clicks |
|----------------|--------|-----------|--------------|
| Solar NSW      | 42     | 18        | — (link pending) |
| Electrical NSW | 38     | 14        | — (link pending) |
```
