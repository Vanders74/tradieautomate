// netlify/functions/business-value-lead.js
// Receives POST from the Tradie Business Value Calculator.
// 1. Adds contact to Brevo list 7 (Business Value Calculator) with valuation attributes.
// 2. Sends a transactional email from info@tradieautomate.com with the personalised estimate + free summary PDF link.
// Returns { success, low, high, emailSent, downloadUrl } — downloadUrl surfaced only when email fails.

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
    const { firstName, email, revenue, staff, systems, recurring, low, high } = JSON.parse(event.body || '{}');

    if (!email || !email.includes('@')) {
      return {
        statusCode: 400,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        body: JSON.stringify({ error: 'Please enter a valid email address.' }),
      };
    }

    const BREVO_API_KEY = process.env.BREVO_API_KEY;
    const summaryUrl = 'https://tradieautomate.com/business-valuation-summary.pdf';

    // 1. Add contact to Brevo list 7 with valuation attributes
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
              BV_REVENUE: revenue != null ? String(revenue) : '',
              BV_STAFF: staff || '',
              BV_SYSTEMS: systems || '',
              BV_RECURRING: recurring || '',
              BV_LOW: low != null ? low : 0,
              BV_HIGH: high != null ? high : 0,
              BV_DATE: new Date().toISOString().split('T')[0],
            },
            listIds: [7],
            updateEnabled: true,
          }),
        });
        if (!res.ok && res.status !== 204) {
          console.error('Brevo contact error:', res.status, await res.text());
        }
      } catch (brevoErr) {
        console.error('Brevo contact request failed:', brevoErr);
      }
    } else {
      console.warn('BREVO_API_KEY not configured — contact not saved');
    }

    // 2. Send transactional email with the personalised estimate
    let emailSent = false;
    let emailError = null;
    if (BREVO_API_KEY) {
      const html = buildEmailHtml({ firstName, email, low, high, summaryUrl });
      const text = buildEmailText({ firstName, low, high, summaryUrl });

      try {
        const res = await fetch('https://api.brevo.com/v3/smtp/email', {
          method: 'POST',
          headers: {
            'api-key': BREVO_API_KEY,
            'Content-Type': 'application/json',
            Accept: 'application/json',
          },
          body: JSON.stringify({
            sender: { name: 'Shane | TradieAutomate', email: 'info@tradieautomate.com' },
            to: [{ email, name: firstName || '' }],
            subject: 'Your Tradie Business Valuation Estimate',
            htmlContent: html,
            textContent: text,
          }),
        });
        emailSent = res.ok || res.status === 201 || res.status === 202;
        if (!emailSent) {
          const errBody = await res.text();
          emailError = `Brevo SMTP ${res.status}: ${errBody}`;
          console.error('Brevo email error:', res.status, errBody);
        }
      } catch (emailErr) {
        emailError = `Request failed: ${emailErr.message || emailErr}`;
        console.error('Brevo email request failed:', emailErr);
      }
    } else {
      emailError = 'BREVO_API_KEY not configured';
    }

    return {
      statusCode: 200,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        success: true,
        low,
        high,
        emailSent,
        emailError,
        downloadUrl: summaryUrl,
      }),
    };
  } catch (err) {
    console.error('business-value-lead error:', err);
    return {
      statusCode: 500,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      body: JSON.stringify({ error: 'Something went wrong. Please try again.' }),
    };
  }
};

function fmtAUD(n) {
  if (n == null || isNaN(n)) return '';
  const v = Math.round(n);
  if (v >= 1000000) return '$' + (v / 1000000).toFixed(2).replace(/\.?0+$/, '') + 'M';
  if (v >= 1000) return '$' + (v / 1000).toFixed(0) + 'K';
  return '$' + v;
}

function buildEmailHtml({ firstName, low, high, summaryUrl }) {
  const name = firstName ? ` ${firstName}` : '';
  const range = (low != null && high != null) ? `${fmtAUD(low)} – ${fmtAUD(high)}` : '';
  return `<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"></head>
<body style="margin:0;padding:0;background:#f4f6f8;font-family:system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;">
  <div style="max-width:560px;margin:0 auto;padding:24px 16px;">
    <div style="background:#0f172a;border-radius:12px 12px 0 0;padding:24px 28px;text-align:center;">
      <div style="font-size:22px;font-weight:800;color:#ffffff;">⚡ TradieAutomate</div>
    </div>
    <div style="background:#ffffff;border-radius:0 0 12px 12px;padding:32px 28px;">
      <h1 style="margin:0 0 6px;font-size:22px;line-height:1.3;color:#0f172a;">Your business valuation estimate is here${name}.</h1>
      ${range ? `<p style="margin:16px 0;font-size:26px;font-weight:800;color:#ea580c;">${range}</p>` : ''}
      <p style="margin:0 0 24px;font-size:15px;line-height:1.6;color:#334155;">
        This range is based on a Seller's Discretionary Earnings (SDE) multiple — the standard method for valuing
        Australian trade businesses. It's an estimate for planning, not a professional valuation.
      </p>
      <a href="${summaryUrl}" style="display:inline-block;background:#f97316;color:#ffffff;padding:14px 28px;border-radius:8px;font-weight:700;font-size:16px;text-decoration:none;">Download your valuation summary &rarr;</a>
      <p style="margin:14px 0 0;font-size:12px;color:#64748b;">Free one-page summary — methodology + your next steps.</p>
      <hr style="border:none;border-top:1px solid #e2e8f0;margin:28px 0;">
      <p style="margin:0;font-size:13px;color:#64748b;line-height:1.6;">
        Want a full breakdown of the method, 2026 trade-business multiples, and a 90-day value-building plan?
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

function buildEmailText({ firstName, low, high, summaryUrl }) {
  const name = firstName ? ` ${firstName}` : '';
  const range = (low != null && high != null) ? `${fmtAUD(low)} – ${fmtAUD(high)}` : '';
  return [
    `Your business valuation estimate is here${name}.`,
    '',
    range,
    '',
    'Based on a Seller\'s Discretionary Earnings (SDE) multiple — the standard method for valuing Australian trade businesses. Estimate for planning, not a professional valuation.',
    '',
    'Download your free one-page summary:',
    summaryUrl,
    '',
    '— TradieAutomate',
  ].join('\n');
}
