// netlify/functions/initiative-stats.js
// Live Brevo list member counts PLUS monetisation-segment bucketing for the
// JOULE (rebates, lists 8-16) and HANDOVER (trade exit, 17-25) initiatives.
// Used by the initiative sub-dashboards so lead growth AND segment value are
// visible without local credentials. Uses BREVO_API_KEY from Netlify env.
// No secrets in repo.

const API = 'https://api.brevo.com/v3';

// Bucket a list of contact objects (with attributes) into monetisation segments.
function bucketJoule(contacts) {
  // JOULE segments = upgrade type (installers pay per lead by product category).
  const seg = {};
  for (const c of contacts) {
    const a = (c && c.attributes) || {};
    const u = String(a.UPGRADE_TYPE || a.upgrade_type || 'unknown').trim();
    seg[u] = (seg[u] || 0) + 1;
  }
  const order = ['heat pump', 'solar', 'battery', 'ev charger', 'heatpump', 'unknown'];
  const keys = Object.keys(seg).sort();
  return { by_upgrade: seg, segments: keys.filter((k) => k !== 'unknown').length, listed: contacts.length };
}

function bucketHandover(contacts) {
  // HANDOVER segments = readiness tiers (what sponsors pay for).
  // Ready: score >=80 (Acquisition-Ready band). Building: 55-79. Early: <55.
  let ready = 0, building = 0, early = 0, unscored = 0;
  for (const c of contacts) {
    const a = (c && c.attributes) || {};
    const s = a.TV_SCORE != null ? Number(a.TV_SCORE) : NaN;
    if (Number.isNaN(s)) { unscored++; continue; }
    if (s >= 80) ready++;
    else if (s >= 55) building++;
    else early++;
  }
  return { ready, building, early, unscored, listed: contacts.length };
}

async function fetchListContacts(key, listId, limit = 300) {
  // Use the contact-search endpoint (returns full attributes), filtered by list.
  const res = await fetch(`${API}/contacts?listIds=${listId}&limit=${limit}&offset=0`, {
    headers: { 'api-key': key, Accept: 'application/json' },
  });
  if (!res.ok) return [];
  const data = await res.json();
  return (data.contacts || []).map((c) => ({ email: c.email, attributes: c.attributes || {} }));
}

async function findListId(lists, namePrefix) {
  const m = lists.find((l) => l.name.startsWith(namePrefix));
  return m ? m.id : null;
}

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
    const all = data.lists || [];

    const lists = {};
    for (const l of all) lists[l.name] = { id: l.id, count: l.totalRecipients || 0 };
    const names = Object.keys(lists).sort();
    const joule = names.filter((n) => n.startsWith('Rebate Leads'));
    const handover = names.filter((n) => n.startsWith('Trade Exit Leads'));
    const total = (arr) => arr.reduce((s, n) => s + (lists[n].count || 0), 0);

    // Fetch master-list contacts for segment bucketing (joule master = first
    // "Rebate Leads" list, handover master = first "Trade Exit Leads" list).
    let jouleBucket = { by_upgrade: {}, segments: 0, listed: 0 };
    let handoverBucket = { ready: 0, building: 0, early: 0, unscored: 0, listed: 0 };
    try {
      const jMaster = await findListId(all, 'Rebate Leads');
      const hMaster = await findListId(all, 'Trade Exit Leads');
      if (jMaster) jouleBucket = bucketJoule(await fetchListContacts(key, jMaster));
      if (hMaster) handoverBucket = bucketHandover(await fetchListContacts(key, hMaster));
    } catch (e) {
      // Segment bucketing is best-effort; list counts remain authoritative.
      jouleBucket = { by_upgrade: {}, segments: 0, listed: 0, error: e.message };
      handoverBucket = { ready: 0, building: 0, early: 0, unscored: 0, listed: 0, error: e.message };
    }

    return {
      statusCode: 200,
      headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' },
      body: JSON.stringify({
        available: true,
        fetched_at: new Date().toISOString(),
        lists,
        joule: { lists: joule.map((n) => ({ name: n, count: lists[n].count })), total: total(joule), segments: jouleBucket },
        handover: { lists: handover.map((n) => ({ name: n, count: lists[n].count })), total: total(handover), tiers: handoverBucket },
      }),
    };
  } catch (e) {
    return { statusCode: 500, body: JSON.stringify({ available: false, error: e.message }) };
  }
};