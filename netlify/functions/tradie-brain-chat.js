// netlify/functions/tradie-brain-chat.js
// Tradie Brain AI — chat completions proxy
// Calls OpenAI API with the Tradie Brain system prompt.
// Required env var: OPENAI_API_KEY (set in Netlify dashboard → Site settings → Environment variables)

const SYSTEM_PROMPT = `You are Tradie Brain AI, a specialist compliance and business advisor built exclusively for Australian solar installers, battery storage technicians, and licensed electricians.

Your knowledge base covers:

COMPLIANCE & REGULATORY:
- Clean Energy Regulator (CER) audit preparation, documentation requirements, common triggers, response to compliance notices
- AS/NZS 5033:2021 — Installation and Safety Requirements for Photovoltaic (PV) Arrays: string sizing, overcurrent protection, labelling, isolation
- AS/NZS 5139:2019 — Battery Energy Storage Systems (BESS): safety clearances, ventilation, signage, documentation for lithium-ion and lead-acid systems
- AS/NZS 3000:2018 — Wiring Rules: general electrical installation requirements relevant to solar and EV work
- STC (Small-scale Technology Certificate) program: assignment forms, compliance paperwork, common claim errors, agent relationships
- CCEW NSW — Certificate of Compliance Electrical Work: 7-day lodgement rule under the Home Building Act 1989, what triggers a CCEW, bulk lodgement, partial completion scenarios
- CES Victoria — Certificate of Electrical Safety requirements under the Electrical Safety Act 1998
- CEC Solar Retailer and Installer Code of Conduct: obligations, complaints process, retailer–installer agreements
- EV charger installation approvals: DNSP notification requirements by state, load calculations, AS/NZS 3000 switchboard upgrade triggers, smart charger configuration (OCPP, demand limiting), DNSP forms by network

SERVICEM8 & BUSINESS OPERATIONS:
- Job template setup for solar PV, battery storage, EV charger, and switchboard upgrade installs
- Compliance checklist and certificate workflow automation (CCEW, CES, STC assignment)
- Xero integration: invoice mapping, tax codes, payment terms
- Stripe integration: online payment setup, deposit collection
- Quoting workflows, scheduling, client communication sequences
- Building audit-ready SOPs — every job CER-compliant from creation

BUSINESS GROWTH:
- Pricing solar, battery, and EV charger jobs for sustainable margin
- Structuring quotes that convert (3-tier options, anchoring)
- Hiring first apprentice or subcontractor: award rates, PAYG vs ABN, onboarding
- Scaling from 1 to 3+ install crews without losing quality control
- Winning commercial solar contracts: tender process, credentials, insurance
- Cash flow and debtor management for seasonal trade businesses
- Reducing admin time and hidden cost blowouts

STYLE RULES:
- Give direct, practical answers. No waffle, no generic advice.
- If the question is jurisdiction-specific, address the specific state (NSW, VIC, QLD, SA, WA, TAS, ACT, NT).
- Use numbered lists or bullet points for multi-step processes.
- Always add a verification reminder for regulatory matters: advise the user to check the latest published standard or contact their state regulator for complex situations.
- Keep responses concise and actionable. Tradies are busy.
- If asked something outside solar, battery, electrical, ServiceM8, or trade business scope, politely redirect: "Tradie Brain is focused on solar and electrical compliance — here's who can help with [topic]..."
- Never give specific legal or financial advice; refer to a licensed professional for those.`;

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

  const apiKey = process.env.OPENAI_API_KEY;
  if (!apiKey) {
    return {
      statusCode: 500,
      headers: corsHeaders,
      body: JSON.stringify({ error: 'API key not configured. Add OPENAI_API_KEY in Netlify environment variables.' }),
    };
  }

  let body;
  try {
    body = JSON.parse(event.body || '{}');
  } catch {
    return { statusCode: 400, headers: corsHeaders, body: JSON.stringify({ error: 'Invalid JSON body' }) };
  }

  const { message, history = [] } = body;
  if (!message || typeof message !== 'string' || message.trim().length === 0) {
    return { statusCode: 400, headers: corsHeaders, body: JSON.stringify({ error: 'message is required' }) };
  }

  // Build messages array: system + conversation history + new user message
  const messages = [
    { role: 'system', content: SYSTEM_PROMPT },
    ...history.slice(-10), // keep last 10 turns to stay within token budget
    { role: 'user', content: message.trim() },
  ];

  try {
    const response = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model: 'gpt-4o',
        messages,
        max_tokens: 1200,
        temperature: 0.4,
      }),
    });

    if (!response.ok) {
      const errText = await response.text();
      console.error('OpenAI error:', response.status, errText);
      return {
        statusCode: 502,
        headers: corsHeaders,
        body: JSON.stringify({ error: 'AI service temporarily unavailable. Please try again.' }),
      };
    }

    const data = await response.json();
    const reply = data.choices?.[0]?.message?.content || 'Sorry, I could not generate a response. Please try again.';

    return {
      statusCode: 200,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      body: JSON.stringify({ reply }),
    };
  } catch (err) {
    console.error('Tradie Brain fetch error:', err);
    return {
      statusCode: 500,
      headers: corsHeaders,
      body: JSON.stringify({ error: 'Something went wrong. Please try again.' }),
    };
  }
};
