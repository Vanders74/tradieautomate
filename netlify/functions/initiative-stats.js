// netlify/functions/initiative-stats.js
// Live Brevo list member counts PLUS monetisation-segment bucketing for the
// JOULE (rebates, lists 8-16) and HANDOVER (trade exit, 17-25) initiatives.
// Used by the initiative sub-dashboards so lead growth AND segment value are
// visible without local credentials. Uses BREVO_API_KEY from Netlify env.
// No secrets in repo.

const API = 'https://api.brevo.com/v3';
const PAGE = 1000;

// Bucket contacts (with attributes + listIds) into monetisation segments.
function bucketJoule(contacts, masterId) {
  const seg = {};
  let inList = 0;
  for (const c of contacts) {
    if (!(c.listIds || []).includes(masterId)) continue;
    inList++;
    const a = (c && c.attributes) || {};
    const u = String(a.UPGRADE_TYPE || a.upgrade_type || 'unknown').trim() || 'unknown';
    seg[u] = (seg[u] || 0) + 1;
  }
  return { by_upgrade: seg, segments: Object.keys(seg).filter((k) => k !== 'unknown').length, listed: inList };
}

function bucketHandover(contacts, masterId) {
  let ready = 0, building = 0, early = 0, unscored = 0, inList = 0;
  for (const c of contacts) {
    if (!(c.listIds || []).includes(masterId)) continue;
    inList++;
    const a = (c && c.attributes) || {};
    const s = a.TV_SCORE != null ? Number(a.TV_SCORE) : NaN;
    if (Number.isNaN(s)) { unscored++; continue; }
    if (s >= 80) ready++;
    else if (s >= 55) building++;
    else early++;
  }
  return { ready, building, early, unscored, listed: inList };
}

async function fetchAllContacts(key, limit = 5000) {
  // Paginated crawl of ALL contacts (volume is small right now); each returns
  // attributes + listIds, so bucketing can filter by master-list membership.
  const out = [];
  let offset = 0;
  let lastStatus = null;
  while (true) {
    const res = await fetch(`${API}/contacts?limit=${PAGE}&offset=${offset}&modifiedSince=${encodeURIComponent(new Date(Date.now() - 30 * 864e5).toISOString())}`, {
      headers: { 'api-key': key, Accept: 'application/json' },
    });
    lastStatus = res.status;
    if (!res.ok) break;
    const data = await res.json();
    const batch = (data.contacts || []).map((c) => ({
      email: c.email,
      attributes: c.attributes || {},
      listIds: c.listIds || [],
    }));
    out.push(...batch);
    if (batch.length < limit) break;
    offset += limit;
    if (offset > 20000) break; // safety cap
  }
  out.meta = { lastStatus, pages: Math.ceil(offset / limit) + 1 };
  return out;
}

function findListId(lists, namePrefix) {
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

    // Crawl contacts once; bucket by master-list membership (authoritative,
    // not dependent on Brevo's lagging totalRecipients).
    let jouleBucket = { by_upgrade: {}, segments: 0, listed: 0 };
    let handoverBucket = { ready: 0, building: 0, early: 0, unscored: 0, listed: 0 };
    try {
      const contacts = await fetchAllContacts(key);
      const jMaster = findListId(all, 'Rebate Leads');
      const hMaster = findListId(all, 'Trade Exit Leads');
      if (jMaster) jouleBucket = bucketJoule(contacts, jMaster);
      if (hMaster) handoverBucket = bucketHandover(contacts, hMaster);
      jouleBucket.crawl = contacts.meta;
      handoverBucket.crawl = contacts.meta;
      handoverBucket.crawled = contacts.length;
    } catch (e) {
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