// netlify/functions/trade-exit-lead.js
// Captures Trade Business Valuation report-download leads → Brevo.
// Uses BREVO_API_KEY from Netlify env. Lists are resolved by name at
// runtime (idempotent helper): 'Trade Exit Leads' master + per-state.
// Contacts carry score/trade/horizon attributes for sponsor qualification.

const API = 'https://api.brevo.com/v3';

exports.handler = async (event) => {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method Not Allowed' };
  }

  try {
    const { email, score, trade, horizon, state } = JSON.parse(event.body || '{}');
    if (!email || !email.includes('@')) {
      return { statusCode: 400, body: JSON.stringify({ error: 'Invalid email' }) };
    }

    const key = process.env.BREVO_API_KEY;
    if (!key) {
      console.error('BREVO_API_KEY not configured');
      return { statusCode: 200, body: JSON.stringify({ success: true }) };
    }
    const headers = { 'api-key': key, 'Content-Type': 'application/json', Accept: 'application/json' };

    // Resolve list IDs by name (created via rebate-lists-bootstrap; tolerates renames)
    async function listId(name) {
      const res = await fetch(`${API}/contacts/lists?limit=50&offset=0`, { headers });
      if (!res.ok) return null;
      const data = await res.json();
      const hit = (data.lists || []).find((l) => l.name === name);
      return hit ? hit.id : null;
    }

    const masterId = await listId('Trade Exit Leads');
    let stateListId = null;
    if (state) stateListId = await listId(`Trade Exit Leads - ${state}`);

    const listIds = [masterId].filter((x) => x);
    if (stateListId) listIds.push(stateListId);
    if (!listIds.length) {
      return { statusCode: 200, body: JSON.stringify({ success: true }) }; // no list yet, don't break UX
    }

    const payload = {
      email,
      attributes: {
        TV_SCORE: score != null ? Math.round(score) : undefined,
        TV_TRADE: trade || '',
        TV_HORIZON: horizon || '',
        TV_STATE: state || '',
        LEAD_SOURCE: 'trade-business-valuation',
      },
      listIds,
      updateEnabled: true,
    };
    // strip undefined attrs
    for (const k in payload.attributes) {
      if (payload.attributes[k] === undefined) delete payload.attributes[k];
    }

    const res = await fetch(`${API}/contacts`, { method: 'POST', headers, body: JSON.stringify(payload) });
    if (!res.ok) {
      const text = await res.text();
      console.error('Brevo failed:', res.status, text.slice(0, 200));
      return { statusCode: 502, body: JSON.stringify({ success: false }) };
    }
    return { statusCode: 200, body: JSON.stringify({ success: true }) };
  } catch (e) {
    console.error('trade-exit-lead error:', e.message);
    return { statusCode: 500, body: JSON.stringify({ success: false, error: e.message }) };
  }
};