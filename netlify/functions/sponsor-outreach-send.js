// netlify/functions/sponsor-outreach-send.js
// Sends ONE sponsorship outreach wave via Brevo transactional email.
// Security model (repo is public, so NO secrets in code):
//  - strict recipient ALLOWLIST below (only these addresses can be emailed)
//  - one request = one send; caller supplies company+state to pick template
//  - Brevo daily limits + Netlify function rate limits bound abuse
// Usage: POST /sponsor-outreach-send with JSON { to, company, state, lastName?, template: 1|2|3 }
// Templates: 1=initial pitch, 2=follow-up day3, 3=final/pilot day7

const ALLOW = [
  'hello@reclaimenergy.com.au',
  'info@qis.com.au',
  'sg.info@solargain.com.au',
  'info@renewlec.com.au',
  'support@voltxenergy.com.au',
  'enquiries@fusionsunsolar.com.au',
];

const REBATE_PER_STATE = {
  VIC: { name: 'VEU hot water / Solar Victoria', amount: '$1,000–$1,400', regulator: 'Solar Victoria' },
  NSW: { name: 'ESS hot water upgrade', amount: 'up to $640', regulator: 'NSW Climate and Energy Action' },
  QLD: { name: 'STC discount', amount: '$500–$800', regulator: 'Clean Energy Regulator' },
  SA: { name: 'REPS VPP incentive', amount: 'up to ~$2,050', regulator: 'SA DEW' },
  WA: { name: 'WA Residential Battery Scheme', amount: '$1,300–$3,800 + $10K loan', regulator: 'Energy Policy WA' },
  TAS: { name: 'STC discount (federal)', amount: '$500–$800', regulator: 'Clean Energy Regulator' },
  ACT: { name: 'Sustainable Household Scheme', amount: 'loans up to $20K at ~3%', regulator: 'ACT Government' },
  NT: { name: 'STC discount (federal)', amount: '$500–$800', regulator: 'Clean Energy Regulator' },
};

function template(n, { company, state, firstName }) {
  const r = REBATE_PER_STATE[state] || REBATE_PER_STATE.VIC;
  const price = state === 'VIC' || state === 'NSW' || state === 'QLD' ? 800 : 500;
  const hi = firstName ? `Hi ${firstName},` : 'Hi there,';
  if (n === 1) {
    return {
      subject: `${company} - TradieAutomate rebate leads in ${state}`,
      text: `${hi}\n\nI'm Shane from TradieAutomate - the site Australian tradies and homeowners use for tool comparisons and rebate guidance. We just launched a Rebate Finder that walks homeowners through exactly which rebates they qualify for in their state - heat pumps, solar, batteries - with amounts and expiry dates, verified weekly against the regulator sources.\n\nWhy it matters for ${company}: when a ${state} homeowner searches "${state} rebate 2026" and finishes our quiz, they're about to spend $5,000-$15,000 with an installer. Right now that quiz ends with a "get matched with an installer" CTA.\n\nWe're opening one sponsor slot per state. For $${price}/month you get a fixed placement on every result page a ${state} user sees, shown alongside the ${r.name} (${r.amount}) rebate they're checking - ${r.regulator}-verified. Or if you prefer per-outcome, we're trialing $30 per qualified lead.\n\nThe finder is live: https://tradieautomate.com/tools/rebate-finder/\n\nWould love to walk you through what a ${state} user sees.\n\nShane\nTradieAutomate - info@tradieautomate.com`,
    };
  }
  if (n === 2) {
    return {
      subject: `Re: ${company} + TradieAutomate - ${state} rebate leads`,
      text: `${hi}\n\nQuick follow-up on the sponsor slot for ${state} users on our Rebate Finder.\n\n- The finder now covers all 8 states + federal; ${state} users see the ${r.name} (${r.amount}) first\n- Data re-verified against ${r.regulator} every week by an automated agent\n- Each state is exclusive - first installer in ${state} gets the spot\n\nIf the monthly placement isn't right, the $30/lead trial may suit better - happy to set either up this week.\n\nShane`,
    };
  }
  return {
    subject: `One slot left for ${state} (+ pilot option)`,
    text: `${hi}\n\nLast nudge. We're holding the ${state} slot for ${company} until end of week.\n\nOption we can start Monday: 30-day pilot at half price ($${Math.round(price / 2)}) - you get the placement, we get a case study, and if it doesn't pay for itself you walk away clean.\n\nEither way - worth 10 minutes on the live page: https://tradieautomate.com/tools/rebate-finder/\n\nShane`,
  };
}

exports.handler = async (event) => {
  if (event.httpMethod !== 'POST') return { statusCode: 405, body: 'POST only' };
  const BREVO_API_KEY = process.env.BREVO_API_KEY;
  if (!BREVO_API_KEY) return { statusCode: 500, body: JSON.stringify({ error: 'BREVO_API_KEY not configured' }) };

  let body;
  try { body = JSON.parse(event.body || '{}'); } catch { return { statusCode: 400, body: 'bad json' }; }

  const to = (body.to || '').trim().toLowerCase();
  if (!ALLOW.includes(to)) return { statusCode: 403, body: JSON.stringify({ error: 'recipient not in allowlist' }) };
  const tpl = template(body.template || 1, {
    company: body.company || 'your company',
    state: body.state || 'VIC',
    firstName: body.firstName || '',
  });

  try {
    const res = await fetch('https://api.brevo.com/v3/smtp/email', {
      method: 'POST',
      headers: { 'api-key': BREVO_API_KEY, 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify({
        sender: { name: 'TradieAutomate', email: 'info@tradieautomate.com' },
        to: [{ email: to }],
        subject: tpl.subject,
        textContent: tpl.text,
        tags: ['sponsor-outreach', `state-${body.state}`, `tpl-${body.template || 1}`],
      }),
    });
    const text = await res.text();
    return { statusCode: res.ok ? 200 : 502, body: JSON.stringify({ ok: res.ok, status: res.status, brevo: text.slice(0, 400) }) };
  } catch (e) {
    return { statusCode: 502, body: JSON.stringify({ error: e.message }) };
  }
};