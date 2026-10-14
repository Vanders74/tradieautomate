// netlify/functions/rebate-lead.js
// Captures Rebate Finder lead form submissions → Brevo list (state-routed).
// Reuses BREVO_API_KEY from Netlify env (same as other lead functions).
// Lists (IDs confirmed via rebate-lists-bootstrap): 8=master, 9=VIC, 10=NSW,
// 11=QLD, 12=SA, 13=WA, 14=TAS, 15=ACT, 16=NT
const STATE_LIST = { VIC: 9, NSW: 10, QLD: 11, SA: 12, WA: 13, TAS: 14, ACT: 15, NT: 16 };
const MASTER_LIST = 8;

exports.handler = async (event) => {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method Not Allowed' };
  }

  try {
    const { name, email, postcode, state, upgrade } = JSON.parse(event.body || '{}');
    if (!email || !email.includes('@')) {
      return { statusCode: 400, body: JSON.stringify({ error: 'Invalid email' }) };
    }

    const firstName = name ? name.split(' ')[0] : '';
    const lastName = name ? name.split(' ').slice(1).join(' ') : '';
    const stateList = STATE_LIST[state] || MASTER_LIST;

    const BREVO_API_KEY = process.env.BREVO_API_KEY;
    if (!BREVO_API_KEY) {
      console.error('BREVO_API_KEY not configured in Netlify environment variables');
      return { statusCode: 200, body: JSON.stringify({ success: true }) };
    }

    const headers = { 'api-key': BREVO_API_KEY, 'Content-Type': 'application/json', Accept: 'application/json' };
    const payload = {
      email,
      attributes: {
        FIRSTNAME: firstName,
        LASTNAME: lastName,
        POSTCODE: String(postcode || ''),
        REBATE_STATE: state || '',
        UPGRADE_TYPE: upgrade || '',
        LEAD_SOURCE: 'rebate-finder',
      },
      listIds: [MASTER_LIST, stateList],
      updateEnabled: true,
    };

    const res = await fetch('https://api.brevo.com/v3/contacts', {
      method: 'POST',
      headers,
      body: JSON.stringify(payload),
    });

    if (!res.ok) {
      const text = await res.text();
      console.error('Brevo request failed:', res.status, text.slice(0, 200));
      return { statusCode: 502, body: JSON.stringify({ success: false, error: 'Brevo failed' }) };
    }

    return { statusCode: 200, body: JSON.stringify({ success: true }) };
  } catch (e) {
    console.error('rebate-lead error:', e.message);
    return { statusCode: 500, body: JSON.stringify({ success: false, error: e.message }) };
  }
};