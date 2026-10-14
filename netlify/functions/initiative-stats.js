// netlify/functions/initiative-stats.js
// Live Brevo list member counts PLUS monetisation-segment bucketing for the
// JOULE (rebates, lists 8-16) and HANDOVER (trade exit, 17-25) initiatives.
// Used by the initiative sub-dashboards so lead growth AND segment value are
// visible without local credentials. Uses BREVO_API_KEY from Netlify env.
// No secrets in repo.

const API = 'https://api.brevo.com/v3';
const PAGE = 1000;

// Bucket contact attribute objects into monetisation segments.
function bucketJoule(attrsList, masterId) {
  const seg = {};
  let listed = 0;
  for (const c of attrsList) {
    if (!(c.listIds || []).includes(masterId)) continue;
    listed++;
    const u = String(c.attributes.UPGRADE_TYPE || 'unknown').trim() || 'unknown';
    seg[u] = (seg[u] || 0) + 1;
  }
  return { by_upgrade: seg, segments: Object.keys(seg).filter((k) => k !== 'unknown').length, listed };
}

function bucketHandover(attrsList, masterId) {
  let ready = 0, building = 0, early = 0, unscored = 0, listed = 0;
  for (const c of attrsList) {
    if (!(c.listIds || []).includes(masterId)) continue;
    listed++;
    const s = c.attributes.TV_SCORE != null ? Number(c.attributes.TV_SCORE) : NaN;
    if (Number.isNaN(s)) { unscored++; continue; }
    if (s >= 80) ready++;
    else if (s >= 55) building++;
    else early++;
  }
  return { ready, building, early, unscored, listed };
}

async function getContactDetail(key, email) {
  // Per-contact lookup returns full attributes (the search endpoint omits them).
  try {
    const res = await fetch(`${API}/contacts/${encodeURIComponent(email)}`, {
      headers: { 'api-key': key, Accept: 'application/json' },
    });
    if (!res.ok) return null;
    const d = await res.json();
    return { email, attributes: d.attributes || {}, listIds: d.listIds || [] };
  } catch (e) {
    return null;
  }
}

async function fetchAllContacts(key) {
  // Paginated crawl of ALL contacts (email + listIds only). Volume is small.
  const out = [];
  let offset = 0;
  let lastStatus = null;
  let pages = 0;
  while (true) {
    const res = await fetch(`${API}/contacts?limit=${PAGE}&offset=${offset}&modifiedSince=${encodeURIComponent(new Date(Date.now() - 30 * 864e5).toISOString())}`, {
      headers: { 'api-key': key, Accept: 'application/json' },
    });
    lastStatus = res.status;
    if (!res.ok) break;
    const data = await res.json();
    pages++;
    const batch = (data.contacts || []).map((c) => ({ email: c.email, listIds: c.listIds || [] }));
    out.push(...batch);
    if (batch.length < PAGE) break;
    offset += PAGE;
    if (offset > 20000) break; // safety cap
  }
  out.meta = { lastStatus, pages };
  return out;
}

function findListId(lists, exactName) {
  // EXACT name match — startsWith would catch "Trade Exit Leads - NT" (id 25)
  // before the master "Trade Exit Leads" (id 17) depending on array order.
  const m = lists.find((l) => l.name === exactName);
  return m ? m.id : null;
}

// Resolve full attribute objects for members of a list (parallel lookups).
async function resolveListMembers(key, contacts, masterId, cap = 150) {
  const members = contacts.filter((c) => (c.listIds || []).includes(masterId)).slice(0, cap);
  const chunks = [];
  for (let i = 0; i < members.length; i += 10) chunks.push(members.slice(i, i + 10));
  const resolved = [];
  for (const chunk of chunks) {
    const rs = await Promise.all(chunk.map((c) => getContactDetail(key, c.email)));
    resolved.push(...rs.filter(Boolean));
  }
  return resolved;
}

// Outreach effectiveness: pull recent transactional events, classify by
// recipient email (the reliable key — Brevo event records omit tags), score
// each recipient as sent/delivered/opened/clicked.
const JOULE_RECIPIENTS = [
  'hello@reclaimenergy.com.au', 'info@qis.com.au', 'sg.info@solargain.com.au',
  'info@renewlec.com.au', 'support@voltxenergy.com.au', 'enquiries@fusionsunsolar.com.au',
];
const HANDOVER_RECIPIENTS = [
  'info@fippet.com.au', 'support@workm8consulting.com', 'info@ibsgc.com.au',
  'ask@simplifi.com.au', 'hello@aigain.com.au', 'hello@cotchy.com.au', 'hello@tbateam.com.au',
];

async function fetchOutreachStats(key) {
  const out = { joule: { recipients: 0, delivered: 0, opened: 0, clicked: 0 }, handover: { recipients: 0, delivered: 0, opened: 0, clicked: 0 } };
  try {
    const q = new URLSearchParams({
      limit: '500', offset: '0',
      startDate: '2026-09-01', endDate: new Date().toISOString().slice(0, 10),
    });
    const res = await fetch(`${API}/smtp/statistics/events?${q}`, {
      headers: { 'api-key': key, Accept: 'application/json' },
    });
    if (!res.ok) return out;
    const data = await res.json();
    const events = data.events || [];
    const seen = { joule: {}, handover: {} };

    function classify(email) {
      const e = String(email || '').toLowerCase();
      if (JOULE_RECIPIENTS.includes(e)) return 'joule';
      if (HANDOVER_RECIPIENTS.includes(e)) return 'handover';
      return null;
    }
    for (const e of events) {
      const init = classify(e.email);
      if (!init) continue;
      const email = String(e.email || '').toLowerCase();
      const ev = e.event || '';
      const per = (seen[init][email] = seen[init][email] || { delivered: false, opened: false, clicked: false, opens: 0 });
      if (ev === 'delivered') per.delivered = true;
      if (ev === 'opened') { per.opened = true; per.opens++; }
      if (ev === 'clicks' || ev === 'click') per.clicked = true;
    }
    for (const init of ['joule', 'handover']) {
      const recips = Object.values(seen[init]);
      out[init] = {
        recipients: recips.length,
        delivered: recips.filter((r) => r.delivered).length,
        opened: recips.filter((r) => r.opened).length,
        clicked: recips.filter((r) => r.clicked).length,
        total_opens: recips.reduce((s, r) => s + r.opens, 0),
      };
    }
    out.raw_events = events.length;
  } catch (e) {
    out.error = e.message;
  }
  return out;
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

    let jouleBucket = { by_upgrade: {}, segments: 0, listed: 0 };
    let handoverBucket = { ready: 0, building: 0, early: 0, unscored: 0, listed: 0 };
    let effectiveness = { joule: { recipients: 0, delivered: 0, opened: 0, clicked: 0 }, handover: { recipients: 0, delivered: 0, opened: 0, clicked: 0 } };
    try {
      const contacts = await fetchAllContacts(key);
      const jMaster = findListId(all, 'Rebate Leads');
      const hMaster = findListId(all, 'Trade Exit Leads');
      const [jMembers, hMembers] = await Promise.all([
        jMaster ? resolveListMembers(key, contacts, jMaster) : Promise.resolve([]),
        hMaster ? resolveListMembers(key, contacts, hMaster) : Promise.resolve([]),
      ]);
      if (jMaster) jouleBucket = bucketJoule(jMembers, jMaster);
      if (hMaster) handoverBucket = bucketHandover(hMembers, hMaster);
      jouleBucket.crawl = contacts.meta;
      handoverBucket.crawl = contacts.meta;
      handoverBucket.crawled = contacts.length;
      handoverBucket.masterId = hMaster;
      handoverBucket.jouleMaster = jMaster;
      effectiveness = await fetchOutreachStats(key);
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
        joule: { lists: joule.map((n) => ({ name: n, count: lists[n].count })), total: total(joule), segments: jouleBucket, effectiveness: effectiveness.joule },
        handover: { lists: handover.map((n) => ({ name: n, count: lists[n].count })), total: total(handover), tiers: handoverBucket, effectiveness: effectiveness.handover },
      }),
    };
  } catch (e) {
    return { statusCode: 500, body: JSON.stringify({ available: false, error: e.message }) };
  }
};