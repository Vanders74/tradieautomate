// netlify/functions/initiative-stats.js
// Returns live Brevo list member counts for the JOULE (rebates, 8-16) and
// HANDOVER (trade exit, 17-25) initiative lists. Used by the initiative
// sub-dashboards so lead growth is visible without local credentials.
// Uses BREVO_API_KEY from Netlify env. No secrets in repo.

const API = 'https://api.brevo.com/v3';

exports.handler = async () => {
  const key = process.env.BREVO_API_KEY;
  if (!key) {
    return { statusCode: 200, body: JSON.stringify({ available: false, error: 'BREVO_API_KEY not configured' }) };
  }

  try {
    const res = await fetch(`${API}/contacts/lists?limit=50&offset=0`, {
      headers: { 'api-key': key, Accept: 'application/json' },
    });
    if (!res.ok) {
      return { statusCode: 502, body: JSON.stringify({ available: false, error: `Brevo ${res.status}` }) };
    }
    const data = await res.json();

    const lists = {};
    for (const l of data.lists || []) {
      lists[l.name] = { id: l.id, count: l.totalRecipients || 0 };
    }
    const names = Object.keys(lists).sort();
    const joule = names.filter((n) => n.startsWith('Rebate Leads'));
    const handover = names.filter((n) => n.startsWith('Trade Exit Leads'));
    const total = (arr) => arr.reduce((s, n) => s + (lists[n].count || 0), 0);

    return {
      statusCode: 200,
      headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' },
      body: JSON.stringify({
        available: true,
        fetched_at: new Date().toISOString(),
        lists,
        joule: { lists: joule.map((n) => ({ name: n, count: lists[n].count })), total: total(joule) },
        handover: { lists: handover.map((n) => ({ name: n, count: lists[n].count })), total: total(handover) },
      }),
    };
  } catch (e) {
    return { statusCode: 500, body: JSON.stringify({ available: false, error: e.message }) };
  }
};