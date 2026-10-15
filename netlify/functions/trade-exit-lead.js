// netlify/functions/trade-exit-lead.js
// Captures Trade Business Valuation report-download leads → Brevo.
// 1. Adds contact to 'Trade Exit Leads' master + per-state lists (name-resolved).
// 2. Sends a personalised summary email (score, range, band, top actions).
// Uses BREVO_API_KEY from Netlify env. No secrets in repo (public).

const API = 'https://api.brevo.com/v3';

exports.handler = async (event) => {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method Not Allowed' };
  }

  try {
    const { email, score, trade, horizon, state, low, high, band, actions, token } = JSON.parse(event.body || '{}');
    if (!email || !email.includes('@')) {
      return { statusCode: 400, body: JSON.stringify({ error: 'Invalid email' }) };
    }

    const diagnostics = {};

    // Deep-link: the emailed "View my results" button must land on the user's
    // actual report, not a blank quiz. Token = base64url({a: answers}).
    const reportUrl = 'https://tradieautomate.com/tools/trade-business-valuation/'
      + (token && /^[A-Za-z0-9_-]+$/.test(token) ? '?r=' + token : '');

    const key = process.env.BREVO_API_KEY;
    if (!key) {
      console.error('BREVO_API_KEY not configured');
      return { statusCode: 200, body: JSON.stringify({ success: true }) };
    }
    const headers = { 'api-key': key, 'Content-Type': 'application/json', Accept: 'application/json' };

    // Resolve list IDs by name (created via rebate-lists-bootstrap; tolerates renames)
    async function listId(name) {
      const res = await fetch(`${API}/contacts/lists?limit=50&offset=0`, { headers });
      if (!res.ok) return null;
      const data = await res.json();
      const hit = (data.lists || []).find((l) => l.name === name);
      return hit ? hit.id : null;
    }

    const masterId = await listId('Trade Exit Leads');
    let stateListId = null;
    if (state) stateListId = await listId(`Trade Exit Leads - ${state}`);

    const listIds = [masterId].filter((x) => x);
    if (stateListId) listIds.push(stateListId);

    // Declare the TV_* contact attributes if Brevo doesn't know them yet.
    // Brevo silently DROPS undeclared custom attributes on contact create, so
    // without this the lead lands in the list but TV_SCORE/TV_BAND etc. are
    // never stored — which breaks the entire tier-pricing model.
    const ATTRS = {
      TV_SCORE: 'float', TV_TRADE: 'text', TV_HORIZON: 'text',
      TV_STATE: 'text', TV_BAND: 'text', LEAD_SOURCE: 'text',
    };
    diagnostics.attr_declares = {};
    for (const [name, type] of Object.entries(ATTRS)) {
      try {
        const ar = await fetch(`${API}/contacts/attributes/${encodeURIComponent(name)}`, {
          method: 'POST', headers, body: JSON.stringify({ type, calculated: false }),
        });
        diagnostics.attr_declares[name] = { status: ar.status, body: (await ar.text()).slice(0, 160) };
      } catch (e) {
        diagnostics.attr_declares[name] = { error: e.message };
      }
    }
    // Confirm what Brevo actually lists as known attributes
    try {
      const al = await fetch(`${API}/contacts/attributes`, { headers });
      const ad = await al.json();
      diagnostics.known_attrs = (ad.attributes || []).map((a) => a.name);
    } catch (e) {
      diagnostics.known_attrs_error = e.message;
    }

    if (listIds.length) {
      const payload = {
        email,
        attributes: {
          TV_SCORE: score != null ? Math.round(score) : undefined,
          TV_TRADE: trade || '',
          TV_HORIZON: horizon || '',
          TV_STATE: state || '',
          TV_BAND: band || '',
          LEAD_SOURCE: 'trade-business-valuation',
        },
        listIds,
        updateEnabled: true,
      };
      // strip undefined attrs
      for (const k in payload.attributes) {
        if (payload.attributes[k] === undefined) delete payload.attributes[k];
      }

      try {
        const res = await fetch(`${API}/contacts`, { method: 'POST', headers, body: JSON.stringify(payload) });
        const rtxt = (await res.text()).slice(0, 300);
        if (!res.ok) console.error('Brevo contact failed:', res.status, rtxt);
        else diagnostics.contact_status = res.status;
        diagnostics.contact_body = rtxt;
      } catch (e) {
        console.error('Brevo contact request failed:', e.message);
        diagnostics.contact_error = e.message;
      }
    }

    // Send personalised summary email (same pattern as the legacy business-value-lead summary)
    let emailSent = false;
    try {
      const html = buildEmailHtml({ score, low, high, band, actions, reportUrl });
      const text = buildEmailText({ score, low, high, band, actions, reportUrl });
      const res = await fetch(`${API}/smtp/email`, {
        method: 'POST',
        headers,
        body: JSON.stringify({
          sender: { name: 'Shane | TradieAutomate', email: 'info@tradieautomate.com' },
          to: [{ email }],
          subject: `Your Tradie Business Valuation Estimate`,
          htmlContent: html,
          textContent: text,
        }),
      });
      emailSent = res.ok || res.status === 201 || res.status === 202;
      if (!emailSent) console.error('Brevo email failed:', res.status, (await res.text()).slice(0, 200));
    } catch (e) {
      console.error('Brevo email request failed:', e.message);
    }

    return {
      statusCode: 200,
      body: JSON.stringify({ success: true, emailSent, diagnostics }),
    };
  } catch (e) {
    console.error('trade-exit-lead error:', e.message);
    return { statusCode: 500, body: JSON.stringify({ success: false, error: e.message }) };
  }
};

function fmtAUD(n) {
  if (n == null || isNaN(n)) return '';
  const v = Math.round(n);
  if (v >= 1000000) return '$' + (v / 1000000).toFixed(2).replace(/\.?0+$/, '') + 'M';
  if (v >= 1000) return '$' + (v / 1000).toFixed(0) + 'K';
  return '$' + v;
}

function buildEmailHtml({ score, low, high, band, actions, reportUrl }) {
  const range = low != null && high != null ? `${fmtAUD(low)} – ${fmtAUD(high)}` : '';
  const link = reportUrl || 'https://tradieautomate.com/tools/trade-business-valuation/';
  const actionList = actions
    ? actions.split('|').filter(Boolean).map((a) => `<li style="margin-bottom:6px;">${a}</li>`).join('')
    : '';
  return `<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"></head>
<body style="margin:0;padding:0;background:#f4f6f8;font-family:system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;">
  <div style="max-width:560px;margin:0 auto;padding:24px 16px;">
    <div style="background:#0f172a;border-radius:12px 12px 0 0;padding:24px 28px;text-align:center;">
      <div style="font-size:22px;font-weight:800;color:#ffffff;">⚡ TradieAutomate</div>
    </div>
    <div style="background:#ffffff;border-radius:0 0 12px 12px;padding:32px 28px;">
      <h1 style="margin:0 0 6px;font-size:22px;line-height:1.3;color:#0f172a;">Your business valuation estimate is here.</h1>
      <p style="margin:14px 0;font-size:15px;line-height:1.6;color:#334155;">
        Sellability score: <strong style="font-size:20px;color:#0f172a;">${score != null ? score + '/100' : '—'}</strong>
        ${band ? ` &middot; ${band}` : ''}
      </p>
      ${range ? `<p style="margin:16px 0;font-size:26px;font-weight:800;color:#ea580c;">${range}</p>` : ''}
      ${actionList ? `<p style="margin:0 0 8px;font-size:14px;font-weight:700;color:#0f172a;">Ways to lift your sale price:</p><ul style="margin:0 0 24px;padding-left:20px;font-size:14px;line-height:1.6;color:#334155;">${actionList}</ul>` : ''}
      <p style="margin:0 0 24px;font-size:14px;line-height:1.6;color:#334155;">
        This range is based on a Seller's Discretionary Earnings (SDE) multiple — the standard method for valuing
        Australian trade businesses. It's an estimate for planning, not a professional valuation.
      </p>
      <a href="${link}" style="display:inline-block;background:#f97316;color:#ffffff;padding:14px 28px;border-radius:8px;font-weight:700;font-size:16px;text-decoration:none;">View my results &rarr;</a>
    </div>
    <p style="text-align:center;font-size:12px;color:#94a3b8;margin:20px 0 0;">
      TradieAutomate &middot; Australian trade business systems &middot;
      <a href="https://tradieautomate.com" style="color:#94a3b8;">tradieautomate.com</a>
    </p>
  </div>
</body>
</html>`;
}

function buildEmailText({ score, low, high, band, actions, reportUrl }) {
  const range = low != null && high != null ? `${fmtAUD(low)} - ${fmtAUD(high)}` : '';
  const link = reportUrl || 'https://tradieautomate.com/tools/trade-business-valuation/';
  const lines = [
    'Your business valuation estimate is here.',
    '',
    `Sellability score: ${score != null ? score + '/100' : '—'}${band ? ' (' + band + ')' : ''}`,
  ];
  if (range) lines.push('', `Indicative range: ${range}`);
  if (actions) {
    const list = actions.split('|').filter(Boolean);
    if (list.length) {
      lines.push('', 'Ways to lift your sale price:');
      list.forEach((a) => lines.push(' - ' + a));
    }
  }
  lines.push('', 'This is an estimate for planning, not a professional valuation.', '', 'View your results:', link, '', '— TradieAutomate');
  return lines.join('\n');
}