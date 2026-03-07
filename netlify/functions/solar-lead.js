// netlify/functions/solar-lead.js
// Receives POST from tradieautomate.com/solar form
// Adds contact to Brevo list ID 3 (Solar VIC Outreach)

exports.handler = async (event) => {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method Not Allowed' };
  }

  try {
    const { name, email } = JSON.parse(event.body || '{}');

    if (!email || !email.includes('@')) {
      return { statusCode: 400, body: JSON.stringify({ error: 'Invalid email' }) };
    }

    const firstName = name ? name.split(' ')[0] : '';
    const lastName = name ? name.split(' ').slice(1).join(' ') : '';

    const BREVO_API_KEY = process.env.BREVO_API_KEY;

    if (!BREVO_API_KEY) {
      console.error('BREVO_API_KEY not configured in Netlify environment variables');
      // Return success anyway so UX isn't broken
      return { statusCode: 200, body: JSON.stringify({ success: true }) };
    }

    const res = await fetch('https://api.brevo.com/v3/contacts', {
      method: 'POST',
      headers: {
        'api-key': BREVO_API_KEY,
        'Content-Type': 'application/json',
        Accept: 'application/json',
      },
      body: JSON.stringify({
        email,
        attributes: {
          FIRSTNAME: firstName,
          LASTNAME: lastName,
        },
        listIds: [3],
        updateEnabled: true,
      }),
    });

    if (res.ok || res.status === 204) {
      return {
        statusCode: 200,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ success: true }),
      };
    }

    const errBody = await res.text();
    console.error('Brevo error:', res.status, errBody);
    // Return success to avoid blocking UX
    return { statusCode: 200, body: JSON.stringify({ success: true }) };

  } catch (err) {
    console.error('solar-lead error:', err);
    return { statusCode: 200, body: JSON.stringify({ success: true }) };
  }
};
