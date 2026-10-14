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
    const { email, score, trade, horizon, state, low, high, band, actions } = JSON.parse(event.body || '{}');
    if (!email || !email.includes('@')) {
      return { statusCode: 400, body: JSON.stringify({ error: 'Invalid email' }) };
    }

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
        if (!res.ok) console.error('Brevo contact failed:', res.status, (await res.text()).slice(0, 200));
      } catch (e) {
        console.error('Brevo contact request failed:', e.message);
      }
    }

    // Send personalised summary email (same pattern as the legacy business-value-lead summary)
    let emailSent = false;
    try {
      const html = buildEmailHtml({ score, low, high, band, actions });
      const text = buildEmailText({ score, low, high, band, actions });
      const res = await fetch(`${API}/smtp/email`, {
        method: 'POST',
        headers,
        body: JSON.stringify({
          sender: { name: 'Shane | TradieAutomate', email: 'info@tradieautomate.com' },
          to: [{ email }],
          subject: `Your Trade Business Valuation: ${band || 'Sellability'} report`,
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
      body: JSON.stringify({ success: true, emailSent }),
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

function buildEmailHtml({ score, low, high, band, actions }) {
  const range = low != null && high != null ? `${fmtAUD(low)} - ${fmtAUD(high)}` : '';
  const actionList = actions
    ? actions.split('|').filter(Boolean).map((a) => `<li style="margin-bottom:8px;">${a}</li>`).join('')
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
      <h1 style="margin:0 0 6px;font-size:22px;line-height:1.3;color:#0f172a;">Your sellability report is ready</h1>
      <p style="margin:14px 0;font-size:15px;line-height:1.6;color:#334155;">
        Your sellability score: <strong style="font-size:22px;color:#0f172a;">${score != null ? score + '/100' : '—'}</strong>
        ${band ? ` &middot; <strong>${band}</strong>` : ''}
      </p>
      ${range ? `<p style="margin:16px 0;font-size:26px;font-weight:800;color:#ea580c;">Indicative range: ${range}</p>` : ''}
      ${actionList ? `<p style="margin:0 0 10px;font-size:14px;font-weight:700;color:#0f172a;">Top ways to lift your multiple:</p><ul style="margin:0 0 24px;padding-left:20px;font-size:14px;line-height:1.6;color:#334155;">${actionList}</ul>` : ''}
      <a href="https://tradieautomate.com/tools/trade-business-valuation/" style="display:inline-block;background:#f97316;color:#ffffff;padding:14px 28px;border-radius:8px;font-weight:700;font-size:16px;text-decoration:none;">View my full report &rarr;</a>
      <p style="margin:14px 0 0;font-size:12px;color:#64748b;">Free 12-question scorecard &mdash; estimate for planning only, not a professional valuation.</p>
      <hr style="border:none;border-top:1px solid #e2e8f0;margin:28px 0;">
      <p style="margin:0;font-size:13px;color:#64748b;line-height:1.6;">
        Want the complete method, 2026 multiples and a 90-day value-building plan?
        <a href="https://payhip.com/tradieautomate" style="color:#1a56db;text-decoration:underline;">Upgrade to the Full Valuation Report</a>.
      </p>
    </div>
    <p style="text-align:center;font-size:12px;color:#94a3b8;margin:20px 0 0;">
      TradieAutomate &middot; Australian trade business systems &middot;
      <a href="https://tradieautomate.com" style="color:#94a3b8;">tradieautomate.com</a>
    </p>
  </div>
</body>
</html>`;
}

function buildEmailText({ score, low, high, band, actions }) {
  const range = low != null && high != null ? `${fmtAUD(low)} - ${fmtAUD(high)}` : '';
  const lines = [
    'Your sellability report is ready.',
    '',
    `Sellability score: ${score != null ? score + '/100' : '—'}${band ? ' (' + band + ')' : ''}`,
  ];
  if (range) lines.push('', `Indicative range: ${range}`);
  if (actions) {
    const list = actions.split('|').filter(Boolean);
    if (list.length) {
      lines.push('', 'Top ways to lift your multiple:');
      list.forEach((a) => lines.push(' - ' + a));
    }
  }
  lines.push('', 'View your full report:', 'https://tradieautomate.com/tools/trade-business-valuation/', '', '— TradieAutomate');
  return lines.join('\n');
}