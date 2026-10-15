// netlify/functions/sponsor-outreach-send.js
// Sends ONE sponsorship outreach wave via Brevo transactional email.
// Security model (repo is public, so NO secrets in code):
//  - strict recipient ALLOWLIST below (only these addresses can be emailed)
//  - one request = one send; caller supplies company+state to pick template
//  - Brevo daily limits + Netlify function rate limits bound abuse
// Usage: POST /sponsor-outreach-send with JSON { to, company, state, initiative?, lastName?, template }
// Templates (initiative=default 'joule'): 1=initial, 2=follow-up day3, 3=final day7 (rebates)
// Templates (initiative='handover'): 4=initial, 5=follow-up day3, 6=final day7, 7=founder first-mover (warm opens)

const ALLOW = [
  // JOULE — rebate sponsor pitches (wave 1, 2026-10-14)
  'hello@reclaimenergy.com.au',
  'info@qis.com.au',
  'sg.info@solargain.com.au',
  'info@renewlec.com.au',
  'support@voltxenergy.com.au',
  'enquiries@fusionsunsolar.com.au',
  // HANDOVER — Pool A (warm ServiceM8 partners + trade accountants), verified on official sites 2026-10-14
  'info@fippet.com.au',                 // FiPPeT — ServiceM8 GOLD Partner, VIC
  'support@workm8consulting.com',       // WorkM8 Consulting — ServiceM8 GOLD Partner, NSW
  'info@ibsgc.com.au',                  // Invisible Business Solutions — GOLD + Xero + Mgmt Acct, QLD
  'ask@simplifi.com.au',                // Simplifi — GOLD Partner, SA/WA
  'hello@aigain.com.au',                // AIGain — Tasmania's only SM8 Certified Partner
  'hello@cotchy.com.au',                // Cotchy — national trade accountants/bookkeeping
  'hello@tbateam.com.au',               // Trade Business Accountants — QLD (tax, books + coaching)
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

function template(n, { company, state, initiative }) {
  const hi = 'Hi there,';
  const price = 600;
  if (initiative === 'handover') return handoverTemplate(n, { company, state, hi, price });
  const r = REBATE_PER_STATE[state] || REBATE_PER_STATE.VIC;
  const pr = state === 'VIC' || state === 'NSW' || state === 'QLD' ? 800 : 500;
  if (n === 1) {
    return {
      subject: `${company} - TradieAutomate rebate leads in ${state}`,
      text: `${hi}\n\nI'm Shane from TradieAutomate - the site Australian tradies and homeowners use for tool comparisons and rebate guidance. We just launched a Rebate Finder that walks homeowners through exactly which rebates they qualify for in their state - heat pumps, solar, batteries - with amounts and expiry dates, verified weekly against the regulator sources.\n\nWhy it matters for ${company}: when a ${state} homeowner searches "${state} rebate 2026" and finishes our quiz, they're about to spend $5,000-$15,000 with an installer. Right now that quiz ends with a "get matched with an installer" CTA.\n\nWe're opening one sponsor slot per state. For $${pr}/month you get a fixed placement on every result page a ${state} user sees, shown alongside the ${r.name} (${r.amount}) rebate they're checking - ${r.regulator}-verified. Or if you prefer per-outcome, we're trialing $30 per qualified lead.\n\nThe finder is live: https://tradieautomate.com/tools/rebate-finder/\n\nWould love to walk you through what a ${state} user sees.\n\nShane\nTradieAutomate - info@tradieautomate.com`,
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
    text: `${hi}\n\nLast nudge. We're holding the ${state} slot for ${company} until end of week.\n\nOption we can start Monday: 30-day pilot at half price ($${Math.round(pr / 2)}) - you get the placement, we get a case study, and if it doesn't pay for itself you walk away clean.\n\nEither way - worth 10 minutes on the live page: https://tradieautomate.com/tools/rebate-finder/\n\nShane`,
  };
}

function handoverTemplate(n, { company, state, hi, price }) {
  const tagline = `${company} already helps trade businesses${state ? ` in ${state}` : ''} get their systems, books and teams in order. We built a tool that surfaces those exact gaps - and routes owners to partners like you.`;
  if (n === 4) {
    return {
      subject: `${company} - trade owners with weak systems, sent to you`,
      text: `${hi}\n\nI'm Shane from TradieAutomate - the site Australian tradies use for tools, guides and software comparisons (we've published in-depth reviews of ServiceM8, Tradify, simPRO and the business side of running a trade).\n\nWe just launched a Sellability Scorecard that asks trade owners 12 questions and tells them what their business is worth - and the gaps that are costing them at sale time. When a scorecard flags weak systems, bookkeeping or owner-dependence, owners are told exactly what to fix.\n\n${tagline}\n\nWe're taking one sponsor per category per state on the scorecard results page. Practical example: when an electrician's results show a low systems score, the partner shown beside it to help is a ServiceM8 implementation specialist. Low financial-health score? A trade accountant. It's matchmaking - users get a qualified, pre-warmed partner; you get a lead who already knows they have the problem.\n\nPlacement is $${price}/month per state-category slot, or a pilot for the first 30 days at half ($300). The tool is live: https://tradieautomate.com/tools/trade-business-valuation/\n\nHappy to walk you through what a scorecard result looks like.\n\nShane\nTradieAutomate - info@tradieautomate.com`,
    };
  }
  if (n === 5) {
    return {
      subject: `Re: ${company} + TradieAutomate scorecard leads`,
      text: `${hi}\n\nQuick follow-up on the partnership slot on our Sellability Scorecard.\n\n- Owners get a sale-price range + report card across 8 value drivers (systems, books, independence, compliance...)\n- Your category is matched to the exact gap their results flag - a warm, self-qualified referral\n- Exclusive per state-category; we also run the site's trade-exit guides, so the placement compounds\n\nIf a monthly slot isn't the right shape, we can start with a 30-day pilot at $300 to see the quality of leads first.\n\nShane`,
    };
  }
  if (n === 6) {
    return {
      subject: `Last chance - ${state || 'your'} category slot on the scorecard`,
      text: `${hi}\n\nLast nudge on the scorecard sponsor slot for ${company}.\n\nOur 30-day pilot ($${Math.round(price / 2)}, exclusive placement, no lock-in) can start Monday. If the leads aren't right for you, you walk away - no obligation.\n\nLive tool: https://tradieautomate.com/tools/trade-business-valuation/\n\nShane`,
    };
  }
  // 7 = founder-deal / first-mover: sent on warm engagement before the
  // generic day-3 follow-up, so the warmest openers get the pilot offer first.
  return {
    subject: `${company} - first-mover rate for ${state || 'your state'} before the slot opens`,
    text: `${hi}\n\nI see ${company} took a look at the Sellability Scorecard - so I'm writing to you before we open the ${state || ''} category slot to anyone else.\n\nFirst-mover deal: $${Math.round(price / 2)}/month for the first 30 days (normally $${price}), exclusive ${state || ''} placement on scorecard results pages. If the leads aren't right for you, walk away at day 30 - no lock-in.\n\nWhy move first: we push real traffic to the scorecard across our trade-exit guides and newsletter in the next two weeks. The first partner in ${state || 'your state'} takes the slot and the case study; we don't re-offer it while they're active.\n\n10 minutes on the calculator shows the lead shape: https://tradieautomate.com/tools/trade-business-valuation/\n\nShane`,
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
  const initiative = body.initiative === 'handover' ? 'handover' : 'joule';
  const tpl = template(body.template || 1, {
    company: body.company || 'your company',
    state: body.state || '',
    initiative,
  });

  try {
    const res = await fetch('https://api.brevo.com/v3/smtp/email', {
      method: 'POST',
      headers: { 'api-key': BREVO_API_KEY, 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify({
        sender: { name: 'Shane | TradieAutomate', email: 'info@tradieautomate.com' },
        to: [{ email: to }],
        subject: tpl.subject,
        textContent: tpl.text,
        tags: ['sponsor-outreach', `initiative-${initiative}`, `state-${body.state || 'na'}`, `tpl-${body.template || 1}`],
      }),
    });
    const text = await res.text();
    return { statusCode: res.ok ? 200 : 502, body: JSON.stringify({ ok: res.ok, status: res.status, brevo: text.slice(0, 400) }) };
  } catch (e) {
    return { statusCode: 502, body: JSON.stringify({ error: e.message }) };
  }
};