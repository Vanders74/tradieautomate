// netlify/functions/exit-readiness-lead.js
// Receives POST from Exit-Readiness Quiz widget
// Adds contact to Brevo list 6 (Exit Readiness Quiz) with quiz answers as attributes
// Returns success + custom action plan URL

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
    const { firstName, email, score, tier, answers } = JSON.parse(event.body || '{}');

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
        // Build answer summary for Brevo attributes
        const answerSummary = Object.entries(answers || {})
          .map(([q, a]) => `Q${q}: ${a}`)
          .join(' | ');

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
              QUIZ_SCORE: score,
              QUIZ_TIER: tier,
              QUIZ_ANSWERS: answerSummary.substring(0, 500),
              QUIZ_DATE: new Date().toISOString().split('T')[0],
            },
            listIds: [6],
            updateEnabled: true,
          }),
        });
        if (!res.ok && res.status !== 204) {
          const body = await res.text();
          console.error('Brevo error:', res.status, body);
        }
      } catch (brevoErr) {
        console.error('Brevo request failed:', brevoErr);
      }
    } else {
      console.warn('BREVO_API_KEY not configured — contact not saved');
    }

    // Determine action plan URL based on tier
    const planUrls = {
      'high-risk': '/exit-readiness-plan-high-risk.pdf',
      'scaling-trap': '/exit-readiness-plan-scaling-trap.pdf',
      'exit-ready': '/exit-readiness-plan-exit-ready.pdf',
    };
    const planUrl = planUrls[tier] || '/exit-readiness-plan-scaling-trap.pdf';

    return {
      statusCode: 200,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        success: true,
        score,
        tier,
        downloadUrl: planUrl,
      }),
    };
  } catch (err) {
    console.error('exit-readiness-lead error:', err);
    return {
      statusCode: 500,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      body: JSON.stringify({ error: 'Something went wrong. Please try again.' }),
    };
  }
};