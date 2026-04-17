// netlify/functions/compliance-lead.js
// Receives POST from tradieautomate.com/compliance-checklist form
// Adds contact to Brevo list 4 (Compliance PDF Downloads)
// Returns success + download URL so frontend can reveal the PDF link

exports.handler = async (event) => {
  const corsHeaders = {
    'Access-Control-Allow-Origin': 'https://tradieautomate.com',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
  };

  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 204, headers: corsHeaders, body: '' };
  }

  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, headers: corsHeaders, body: 'Method Not Allowed' };
  }

  try {
    const { firstName, email } = JSON.parse(event.body || '{}');

    if (!email || !email.includes('@')) {
      return {
        statusCode: 400,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        body: JSON.stringify({ error: 'Please enter a valid email address.' }),
      };
    }

    const BREVO_API_KEY = process.env.BREVO_API_KEY;

    if (BREVO_API_KEY) {
      try {
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
              FIRSTNAME: firstName || '',
            },
            listIds: [4],
            updateEnabled: true,
          }),
        });
        if (!res.ok && res.status !== 204) {
          const body = await res.text();
          console.error('Brevo error:', res.status, body);
        }
      } catch (brevoErr) {
        console.error('Brevo request failed:', brevoErr);
        // Don't fail the user request — still give them the PDF
      }
    } else {
      console.warn('BREVO_API_KEY not configured — contact not saved');
    }

    return {
      statusCode: 200,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        success: true,
        downloadUrl: '/solar-compliance-checklist-2026.pdf',
      }),
    };
  } catch (err) {
    console.error('compliance-lead error:', err);
    return {
      statusCode: 500,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      body: JSON.stringify({ error: 'Something went wrong. Please try again.' }),
    };
  }
};
