// netlify/functions/rebate-lists-bootstrap.js
// ONE-TIME bootstrap: ensures Brevo contact lists exist for the Rebate Finder.
// Idempotent — safe to call repeatedly. No secrets committed: uses BREVO_API_KEY
// from Netlify env (already used by the lead functions).
// Call: GET https://tradieautomate.com/.netlify/functions/rebate-lists-bootstrap
// Returns JSON of { listName: listId } for all lists created/found.

const LISTS = [
  'Rebate Leads',
  'Rebate Leads - VIC',
  'Rebate Leads - NSW',
  'Rebate Leads - QLD',
  'Rebate Leads - SA',
  'Rebate Leads - WA',
  'Rebate Leads - TAS',
  'Rebate Leads - ACT',
  'Rebate Leads - NT',
];

exports.handler = async (event) => {
  if (event.httpMethod !== 'GET') {
    return { statusCode: 405, body: 'GET only' };
  }
  const BREVO_API_KEY = process.env.BREVO_API_KEY;
  if (!BREVO_API_KEY) {
    return { statusCode: 500, body: JSON.stringify({ error: 'BREVO_API_KEY not configured' }) };
  }

  const headers = {
    'api-key': BREVO_API_KEY,
    'Content-Type': 'application/json',
    Accept: 'application/json',
  };

  // Fetch existing lists (paginated, 50/page — 9 lists fits in one page)
  let existing = {};
  try {
    const res = await fetch('https://api.brevo.com/v3/contacts/lists?limit=50&offset=0', { headers });
    if (!res.ok) {
      return { statusCode: 502, body: JSON.stringify({ error: 'Brevo list fetch failed', status: res.status, text: (await res.text()).slice(0, 300) }) };
    }
    const data = await res.json();
    for (const l of data.lists || []) existing[l.name] = l.id;
  } catch (e) {
    return { statusCode: 502, body: JSON.stringify({ error: e.message }) };
  }

  const results = {};
  const created = [];
  for (const name of LISTS) {
    if (existing[name]) {
      results[name] = existing[name];
      continue;
    }
    try {
      const res = await fetch('https://api.brevo.com/v3/contacts/lists', {
        method: 'POST',
        headers,
        body: JSON.stringify({ name, folderId: 1 }),
      });
      if (res.ok) {
        const data = await res.json();
        results[name] = data.id;
        created.push(name);
      } else {
        // 409 = already exists (race), 400 = name conflict — retry lookup
        const text = await res.text();
        if (res.status === 409 || res.status === 400) {
          const again = await fetch('https://api.brevo.com/v3/contacts/lists?limit=50&offset=0', { headers });
          const d2 = await again.json();
          const hit = (d2.lists || []).find((l) => l.name === name);
          if (hit) { results[name] = hit.id; continue; }
        }
        results[name] = `ERROR:${res.status} ${text.slice(0, 120)}`;
      }
    } catch (e) {
      results[name] = `ERROR:${e.message}`;
    }
  }

  return {
    statusCode: 200,
    body: JSON.stringify({ lists: results, created, env: { hasBrevoKey: true } }, null, 2),
  };
};