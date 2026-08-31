// netlify/functions/exit-readiness-lead.js
// Receives POST from Exit-Readiness Quiz widget.
// 1. Adds contact to Brevo list 6 (Exit Readiness Quiz) with quiz answers as attributes.
// 2. Sends a transactional email from info@tradieautomate.com with the tiered action-plan PDF link.
// Returns success (no download URL in the response — the report arrives by email).

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

    // Tier metadata
    const tiers = {
      'high-risk': {
        label: 'High Key-Person Risk',
        emoji: '🔴',
        plan: '/exit-readiness-plan-high-risk.pdf',
      },
      'scaling-trap': {
        label: 'The Scaling Trap',
        emoji: '🟡',
        plan: '/exit-readiness-plan-scaling-trap.pdf',
      },
      'exit-ready': {
        label: 'Exit-Ready Asset',
        emoji: '🟢',
        plan: '/exit-readiness-plan-exit-ready.pdf',
      },
    };
    const t = tiers[tier] || tiers['scaling-trap'];
    const planUrl = `https://tradieautomate.com${t.plan}`;
    const scoreLabel = score != null ? `${score} / 36` : '';

    // 1. Add contact to Brevo list 6 with quiz attributes
    if (BREVO_API_KEY) {
      try {
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
          console.error('Brevo contact error:', res.status, await res.text());
        }
      } catch (brevoErr) {
        console.error('Brevo contact request failed:', brevoErr);
      }
    } else {
      console.warn('BREVO_API_KEY not configured — contact not saved');
    }

    // 2. Send transactional email with the action-plan link
    let emailSent = false;
    if (BREVO_API_KEY) {
      const html = buildEmailHtml({ firstName, email, score: scoreLabel, tier: t, planUrl });
      const text = buildEmailText({ firstName, score: scoreLabel, tier: t, planUrl });

      try {
        const res = await fetch('https://api.brevo.com/v3/smtp/email', {
          method: 'POST',
          headers: {
            'api-key': BREVO_API_KEY,
            'Content-Type': 'application/json',
            Accept: 'application/json',
          },
          body: JSON.stringify({
            sender: { name: 'TradieAutomate', email: 'info@tradieautomate.com' },
            to: [{ email, name: firstName || '' }],
            subject: `Your Exit-Readiness Action Plan ${scoreLabel ? `(${scoreLabel})` : ''}`,
            htmlContent: html,
            textContent: text,
          }),
        });
        emailSent = res.ok || res.status === 201 || res.status === 202;
        if (!emailSent) {
          console.error('Brevo email error:', res.status, await res.text());
        }
      } catch (emailErr) {
        console.error('Brevo email request failed:', emailErr);
      }
    }

    return {
      statusCode: 200,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        success: true,
        score,
        tier,
        emailSent,
        // Fallback download link — only surfaced to the user if the email fails.
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

function buildEmailHtml({ firstName, score, tier, planUrl }) {
  const name = firstName ? ` ${firstName}` : '';
  return `<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"></head>
<body style="margin:0;padding:0;background:#f4f6f8;font-family:system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;">
  <div style="max-width:560px;margin:0 auto;padding:24px 16px;">
    <div style="background:#0f172a;border-radius:12px 12px 0 0;padding:24px 28px;text-align:center;">
      <div style="font-size:22px;font-weight:800;color:#ffffff;">⚡ TradieAutomate</div>
    </div>
    <div style="background:#ffffff;border-radius:0 0 12px 12px;padding:32px 28px;">
      <div style="font-size:34px;margin-bottom:12px;">${tier.emoji}</div>
      <h1 style="margin:0 0 6px;font-size:22px;line-height:1.3;color:#0f172a;">Your Exit-Readiness Action Plan is ready${name}.</h1>
      ${score ? `<p style="margin:0 0 20px;font-size:15px;color:#475569;">Your result: <strong style="color:#0f172a;">${tier.label}</strong> &mdash; score ${score}.</p>` : `<p style="margin:0 0 20px;font-size:15px;color:#475569;">Your result: <strong style="color:#0f172a;">${tier.label}</strong>.</p>`}
      <p style="margin:0 0 24px;font-size:15px;line-height:1.6;color:#334155;">
        Your personalised one-page plan breaks down your diagnosis and the exact three priorities
        to focus on next &mdash; based on your answers.
      </p>
      <a href="${planUrl}" style="display:inline-block;background:#f97316;color:#ffffff;padding:14px 28px;border-radius:8px;font-weight:700;font-size:16px;text-decoration:none;">Download your action plan &rarr;</a>
      <p style="margin:14px 0 0;font-size:12px;color:#64748b;">This link never expires.</p>
      <hr style="border:none;border-top:1px solid #e2e8f0;margin:28px 0;">
      <p style="margin:0;font-size:13px;color:#64748b;line-height:1.6;">
        Want the full system? Download the free 12-chapter
        <a href="https://tradieautomate.com/playbook" style="color:#1a56db;text-decoration:underline;">Sparky's Playbook</a>.
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

function buildEmailText({ firstName, score, tier, planUrl }) {
  const name = firstName ? ` ${firstName}` : '';
  return [
    `Your Exit-Readiness Action Plan is ready${name}.`,
    '',
    `Result: ${tier.emoji} ${tier.label}${score ? ` — score ${score}` : ''}.`,
    '',
    'Download your personalised plan here:',
    planUrl,
    '',
    'Want the full system? Download the free 12-chapter Sparky\'s Playbook: https://tradieautomate.com/playbook',
    '',
    '— TradieAutomate',
  ].join('\n');
}
