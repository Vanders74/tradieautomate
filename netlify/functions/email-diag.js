// netlify/functions/email-diag.js
// Diagnostic: why is the valuation report email not arriving?
// 1. Sender / domain verification status in Brevo
// 2. DKIM selector Brevo expects (from sender domain details)
// 3. Blocked/suppressed contacts (Brevo silently drops mail to these
//    after a hard bounce or spam complaint — API still returns success)
// 4. Delivery events for recent sends (delivered / blocked / bounced / spam)
// Uses BREVO_API_KEY from Netlify env. No secrets in repo.

const API = 'https://api.brevo.com/v3';

exports.handler = async (event) => {
  const email = (event.queryStringParameters || {}).email || '';
  const key = process.env.BREVO_API_KEY;
  if (!key) return { statusCode: 200, body: JSON.stringify({ error: 'BREVO_API_KEY not configured' }) };
  const headers = { 'api-key': key, Accept: 'application/json' };
  const out = {};

  try {
    // 1. Senders: are they verified?
    const senders = await fetch(`${API}/senders`, { headers }).then((r) => r.json());
    out.senders = (senders.senders || []).map((s) => ({
      id: s.id, name: s.name, email: s.email, active: s.active,
      verified: !s.isDefault && s.active ? true : s.active, isDefault: !!s.isDefault,
    }));

    // 2. Sender domain details incl. DKIM
    const domains = await fetch(`${API}/senders/domains`, { headers }).then((r) => r.json());
    out.domains = (domains.domains || []).map((d) => ({
      name: d.name, authenticated: d.authenticated, verified: d.verified,
      dkimEnabled: d.dkimEnabled, dkimRecord: d.dkimRecord ? { key: d.dkimRecord.key, record: d.dkimRecord.record, type: d.dkimRecord.type } : null,
      spfRecord: d.spfRecord, dmarcRecord: d.dmarcRecord,
    }));

    // 3. Blocked / suppressed contacts (transactional blacklist)
    const blocked = await fetch(`${API}/smtp/blockedContacts?startDate=2026-09-01&endDate=2026-10-14&limit=100&offset=0`, { headers }).then((r) => r.json());
    out.blocked = (blocked.contacts || []).map((c) => ({ email: c.email, reason: c.reason, blockedAt: c.blockedAt }));

    // 4. If an email was given: is it suppressed / blacklisted as a contact?
    if (email) {
      try {
        const contact = await fetch(`${API}/contacts/${encodeURIComponent(email)}`, { headers }).then((r) => (r.ok ? r.json() : null));
        out.contact = contact ? {
          email: contact.email,
          emailBlacklisted: contact.emailBlacklisted,
          unsubscribed: contact.unsubscribed,
          listIds: contact.listIds,
          attributes: contact.attributes && (contact.attributes.LEAD_SOURCE || contact.attributes.TV_SCORE) ? contact.attributes : undefined,
        } : null;
      } catch { out.contact = 'lookup failed'; }
    }

    // 5. Recent transactional events (last sends through this sender)
    try {
      const events = await fetch(`${API}/smtp/statistics/events?limit=30&offset=0&startDate=2026-10-13&endDate=2026-10-14`, { headers }).then((r) => r.json());
      out.events = (events.events || []).map((e) => ({
        email: e.email, event: e.event, date: e.date, subject: (e.subject || '').slice(0, 60), messageId: e.messageId,
        reason: e.reason || '', tag: (e.tags || []).join(','),
      }));
    } catch { out.events = 'unavailable'; }

    return { statusCode: 200, body: JSON.stringify(out) };
  } catch (e) {
    return { statusCode: 500, body: JSON.stringify({ error: e.message }) };
  }
};