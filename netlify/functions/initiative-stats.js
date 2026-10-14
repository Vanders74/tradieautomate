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

// Outreach effectiveness: pull recent transactional events, bucket by the
// initiative-* tag, score each recipient as sent/delivered/opened/clicked.
async function fetchOutreachStats(key) {
  const out = { joule: {}, handover: {} };
  try {
    const q = new URLSearchParams({
      limit: '500', offset: '0',
      startDate: '2026-09-01', endDate: new Date().toISOString().slice(0, 10),
      tag: 'sponsor-outreach',
    });
    const res = await fetch(`${API}/smtp/statistics/events?${q}`, {
      headers: { 'api-key': key, Accept: 'application/json' },
    });
    if (!res.ok) return out;
    const data = await res.json();
    const events = data.events || [];
    const byInitiative = { joule: {}, handover: {} };
    const byTemplate = { joule: {}, handover: {} };
    for (const e of events) {
      const tags = ((e.tags || []).join(',') + ',' + (e.tag || '') + ',');
      let init = tags.includes('initiative-handover') ? 'handover' : tags.includes('initiative-joule') ? 'joule' : null;
      if (!init) continue;
      const email = (e.email || '').toLowerCase();
      const ev = e.event || '';
      const per = (byInitiative[init][email] = byInitiative[init][email] || { sent: false, delivered: false, opened: false, clicked: false, first: e.date, last: e.date });
      if (ev === 'requests' || ev === 'delivered') per.sent = true;
      if (ev === 'delivered') { per.delivered = true; per.sent = true; }
      if (ev === 'opened') per.opened = true;
      if (ev === 'clicks' || ev === 'click') per.clicked = true;
      if (e.date) { if (per.first === e.date) per.first = e.date; per.last = e.date; }
      // template breakdown (tpl-N tag)
      const tm = String(e.tag || '').split(',').map((t) => t.trim()).find((t) => /^tpl-\d/.test(t));
      if (tm) {
        const key2 = tm.replace('tpl-', '');
        const k = (byTemplate[init][key2] = byTemplate[init][key2] || { sent: 0, delivered: 0, opened: 0, clicked: 0 });
        if (ev === 'requests' || ev === 'delivered') k.sent++;
        if (ev === 'delivered') k.delivered++;
        if (ev === 'opened') k.opened++;
        if (ev === 'clicks' || ev === 'click') k.clicked++;
      }
    }
    const summarize = (map) => {
      const recips = Object.values(map);
      return {
        recipients: recips.length,
        delivered: recips.filter((r) => r.delivered).length,
        opened: recips.filter((r) => r.opened).length,
        clicked: recips.filter((r) => r.clicked).length,
        total_opens: recips.reduce((s, r) => s + (r.opened ? 1 : 0), 0),
      };
    };
    out.joule = summarize(byInitiative.joule).recipients ? { ...summarize(byInitiative.joule), by_template: byTemplate.joule } : summarize(byInitiative.joule);
    out.handover = summarize(byInitiative.handover).recipients ? { ...summarize(byInitiative.handover), by_template: byTemplate.handover } : summarize(byInitiative.handover);
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