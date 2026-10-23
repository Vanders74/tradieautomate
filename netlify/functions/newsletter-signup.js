// netlify/functions/newsletter-signup.js
// Captures newsletter subscriptions → Brevo list 26.
// Declares custom attributes first (Brevo silently drops undeclared ones).
// Reuses BREVO_API_KEY from Netlify env.
const NEWSLETTER_LIST = 26;

const ATTR_DECLARE = [
  { name: 'ICP_ROLE', type: 'text' },
  { name: 'ICP_STATE', type: 'text' },
  { name: 'ICP_INTEREST', type: 'text' },
  { name: 'NEWSLETTER_SOURCE', type: 'text' },
];

exports.handler = async (event) => {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method Not Allowed' };
  }

  try {
    const { email, source } = JSON.parse(event.body || '{}');
    if (!email || !email.includes('@') || email.length > 254) {
      return { statusCode: 400, body: JSON.stringify({ error: 'Valid email required' }) };
    }

    const BREVO_API_KEY = process.env.BREVO_API_KEY;
    if (!BREVO_API_KEY) {
      console.error('BREVO_API_KEY not configured');
      return { statusCode: 200, body: JSON.stringify({ success: true }) };
    }

    const headers = {
      'api-key': BREVO_API_KEY,
      'Content-Type': 'application/json',
      Accept: 'application/json',
    };

    // Declare custom attributes if not already present
    for (const attr of ATTR_DECLARE) {
      try {
        const ar = await fetch(
          `https://api.brevo.com/v3/contacts/attributes/normal/${encodeURIComponent(attr.name)}`,
          { method: 'POST', headers, body: JSON.stringify({ type: attr.type }) }
        );
        if (!ar.ok && ar.status !== 400) {
          console.error(`Attribute declare ${attr.name} failed:`, ar.status, (await ar.text()).slice(0, 120));
        }
      } catch (e) {
        console.error(`Attribute declare ${attr.name} errored:`, e.message);
      }
    }

    const payload = {
      email,
      attributes: {
        ICP_ROLE: '',
        ICP_STATE: '',
        ICP_INTEREST: '',
        NEWSLETTER_SOURCE: source || 'unknown',
      },
      listIds: [NEWSLETTER_LIST],
      updateEnabled: true,
    };

    const res = await fetch('https://api.brevo.com/v3/contacts', {
      method: 'POST',
      headers,
      body: JSON.stringify(payload),
    });

    if (!res.ok) {
      const text = await res.text();
      console.error('Brevo contact failed:', res.status, text.slice(0, 200));
      return { statusCode: 502, body: JSON.stringify({ success: false, error: 'Brevo failed' }) };
    }

    return { statusCode: 200, body: JSON.stringify({ success: true }) };
  } catch (e) {
    console.error('newsletter-signup error:', e.message);
    return { statusCode: 500, body: JSON.stringify({ success: false, error: e.message }) };
  }
};
