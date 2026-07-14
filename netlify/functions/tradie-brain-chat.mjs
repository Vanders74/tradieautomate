/**
 * TradieAutomate — Tradie Brain AI Chat Function
 * 
 * Netlify serverless function. POST { message, history } → { reply }
 * Uses Google Gemini Flash 2.0 (free tier: 15 RPM, 1M TPM, 1,500 RPD).
 * 
 * Requires GEMINI_API_KEY in Netlify environment variables.
 * Get a free key at https://aistudio.google.com/apikey
 */

const GEMINI_API_KEY = process.env.GEMINI_API_KEY;
const MODEL = "gemini-2.0-flash";

const SYSTEM_PROMPT = `You are Tradie Brain AI, a compliance and business advisor built exclusively for Australian solar installers, battery storage technicians, and licensed electrical contractors. Your knowledge is focused on the Australian trade and construction sector.

YOUR EXPERTISE:
- Clean Energy Regulator (CER) audit preparation, documentation, and common triggers
- AS/NZS 5033 — Installation and Safety Requirements for Photovoltaic (PV) Arrays
- AS/NZS 5139 — Electrical Installations — Safety of Battery Energy Storage Systems (BESS)
- AS/NZS 3000 — Wiring Rules
- Clean Energy Council (CEC) Solar Retailer and Installer Code of Conduct
- NSW Certificate of Compliance Electrical Work (CCEW) — 7-day lodgement rule under Home Building Act 1989
- Victorian Certificate of Electrical Safety (CES) — requirements under Electrical Safety Act 1998
- Small-scale Technology Certificate (STC) claims, assignment forms, and common rejection reasons
- EV charger installation: load calculations, DNSP notification by state, switchboard upgrades, smart charger configuration
- ServiceM8: job templates for solar/battery installs, compliance checklists, Xero integration, quoting workflows
- Trade business operations: scaling from sole trader to multi-crew, hiring apprentices, cash flow management, debtor days
- Pricing solar and battery jobs, winning commercial contracts, reducing admin overhead

YOUR TONE:
- Direct, practical, and specific. You speak like an experienced tradie who's been on the tools.
- No corporate fluff. No "leverage your synergies." No "holistic solutions."
- Give actionable steps, not theory. Every answer should include something the user can DO.
- Use Australian English (colour, labour, organisation, licence).
- When referencing a standard, give the specific clause or section where possible.
- If you're unsure about something, say so directly — don't bluff.

IMPORTANT RULES:
- Always include a disclaimer when giving compliance advice: remind users to verify against the latest published standards and consult their state electrical regulator for binding rulings.
- Keep responses concise but thorough. Use bullet points or numbered steps for procedures.
- If a question is outside Australian trade/electrical/solar compliance, politely redirect the user.
- Never make up specific dollar figures, penalty amounts, or regulatory deadlines unless you are certain.`;

export default async function handler(req) {
  // CORS preflight
  if (req.method === "OPTIONS") {
    return new Response(null, {
      status: 204,
      headers: corsHeaders(),
    });
  }

  if (req.method !== "POST") {
    return jsonResponse(405, { error: "Method not allowed. Use POST." });
  }

  if (!GEMINI_API_KEY) {
    return jsonResponse(500, { error: "Server configuration error: API key not set." });
  }

  let body;
  try {
    body = await req.json();
  } catch {
    return jsonResponse(400, { error: "Invalid JSON body." });
  }

  const { message, history } = body;
  if (!message || typeof message !== "string" || message.trim().length === 0) {
    return jsonResponse(400, { error: "Message is required." });
  }

  try {
    // Build conversation for Gemini
    const contents = [];

    // System prompt as first user message (Gemini doesn't have native system prompt)
    contents.push({
      role: "user",
      parts: [{ text: SYSTEM_PROMPT }],
    });
    contents.push({
      role: "model",
      parts: [{ text: "Understood. I'm Tradie Brain AI, ready to help with Australian solar, electrical, and compliance questions. What do you need?" }],
    });

    // Conversation history
    if (Array.isArray(history)) {
      for (const msg of history.slice(-10)) {
        const role = msg.role === "assistant" ? "model" : "user";
        contents.push({ role, parts: [{ text: msg.content }] });
      }
    }

    // Current message
    contents.push({ role: "user", parts: [{ text: message }] });

    const response = await fetch(
      `https://generativelanguage.googleapis.com/v1beta/models/${MODEL}:generateContent?key=${GEMINI_API_KEY}`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          contents,
          generationConfig: {
            temperature: 0.7,
            maxOutputTokens: 1024,
            topP: 0.9,
          },
          safetySettings: [
            { category: "HARM_CATEGORY_HARASSMENT", threshold: "BLOCK_ONLY_HIGH" },
            { category: "HARM_CATEGORY_HATE_SPEECH", threshold: "BLOCK_ONLY_HIGH" },
            { category: "HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold: "BLOCK_ONLY_HIGH" },
            { category: "HARM_CATEGORY_DANGEROUS_CONTENT", threshold: "BLOCK_ONLY_HIGH" },
          ],
        }),
      }
    );

    if (!response.ok) {
      const errText = await response.text();
      console.error("Gemini API error:", response.status, errText);
      return jsonResponse(502, { error: "AI service temporarily unavailable. Please try again in a moment." });
    }

    const data = await response.json();
    const reply = data?.candidates?.[0]?.content?.parts?.[0]?.text;

    if (!reply) {
      console.error("Gemini returned no text:", JSON.stringify(data).slice(0, 500));
      return jsonResponse(502, { error: "Could not generate a response. Please try rephrasing your question." });
    }

    return jsonResponse(200, { reply });
  } catch (err) {
    console.error("Chat function error:", err.message);
    return jsonResponse(500, { error: "Internal server error. Please try again." });
  }
}

function jsonResponse(status, body) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { ...corsHeaders(), "Content-Type": "application/json" },
  });
}

function corsHeaders() {
  return {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
  };
}
