#!/usr/bin/env node
/**
 * faq_schema_audit.js — compare JSON-LD FAQ schema (frontmatter `faq:`)
 * against the visible FAQ (H3 questions in the body). Google requires the
 * schema answer to match what the user can see; drift = quoteable wrong facts.
 *
 * Usage: node scripts/faq_schema_audit.js [--fix]
 * Without --fix it only reports. With --fix it rewrites the frontmatter faq
 * list to mirror the visible FAQ (visible content is the ground truth).
 */
const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');

const BLOG = path.join(__dirname, '..', 'src', 'content', 'blog');
const FIX = process.argv.includes('--fix');

function splitFm(txt) {
  if (!txt.startsWith('---')) return [null, txt];
  const end = txt.indexOf('\n---', 3);
  if (end === -1) return [null, txt];
  return [txt.slice(3, end), txt.slice(end + 4)];
}

function visibleFaq(body) {
  const lines = body.split('\n');
  const out = [];
  let inFaq = false, q = null, a = [];
  const flush = () => { if (q) out.push({ question: q, answer: a.join(' ').trim() }); q = null; a = []; };
  for (const ln of lines) {
    // FAQ section heading (## FAQ, ## Frequently Asked Questions, ## Questions)
    if (/^##\s+.*(frequently asked questions|\bFAQ\b|common questions)\s*(\([^)]*\))?\s*$/i.test(ln)) { inFaq = true; continue; }
    if (inFaq && /^##\s+/.test(ln)) { flush(); break; }
    if (!inFaq) continue;
    // Question styles: "### Question?" or "**Question?**"
    const h3 = ln.match(/^###\s+(.*)/);
    if (h3) { flush(); q = h3[1].trim(); continue; }
    const bold = ln.match(/^\*\*(.+?)\*\*\s*$/);
    if (bold && /\?$/.test(bold[1].trim())) { flush(); q = bold[1].trim(); continue; }
    if (q && ln.trim() && !/^(\||---|!|\[)/.test(ln.trim())) a.push(ln.trim());
  }
  flush();
  return out.filter(x => x.question && x.answer);
}

const norm = s => (s || '').toLowerCase().replace(/[^a-z0-9 ]/g, '').replace(/\s+/g, ' ').trim();

function yamlStr(s) {
  // double-quoted YAML, escaping backslashes and quotes
  return '"' + String(s).replace(/\\/g, '\\\\').replace(/"/g, '\\"') + '"';
}

let files = fs.readdirSync(BLOG).filter(f => f.endsWith('.md'));
let stats = { total: files.length, withVisible: 0, withSchema: 0, match: 0, mismatch: 0, schemaNoVisible: 0, visibleNoSchema: 0, fixed: 0, errors: 0 };
const bad = [];

for (const f of files) {
  const p = path.join(BLOG, f);
  const txt = fs.readFileSync(p, 'utf8');
  const [fmRaw, body] = splitFm(txt);
  if (fmRaw === null) continue;
  let data;
  try { data = yaml.load(fmRaw) || {}; } catch (e) { stats.errors++; bad.push([f, 'YAML parse error']); continue; }
  const fmFaq = Array.isArray(data.faq) ? data.faq.filter(x => x && x.question) : [];
  const vis = visibleFaq(body);
  if (vis.length) stats.withVisible++;
  if (fmFaq.length) stats.withSchema++;

  if (!vis.length && fmFaq.length) { stats.schemaNoVisible++; bad.push([f, `schema has ${fmFaq.length} Qs but no visible FAQ`]); continue; }
  if (vis.length && !fmFaq.length) { stats.visibleNoSchema++; bad.push([f, `visible FAQ (${vis.length} Qs) but no schema`]); continue; }

  const fmMap = new Map(fmFaq.map(x => [norm(x.question), norm(x.answer)]));
  const visMap = new Map(vis.map(x => [norm(x.question), norm(x.answer)]));
  let mismatch = false;
  for (const [q, a] of visMap) {
    if (!fmMap.has(q) || fmMap.get(q).slice(0, 100) !== a.slice(0, 100)) { mismatch = true; break; }
  }
  if (fmMap.size !== visMap.size) mismatch = true;

  if (mismatch) {
    stats.mismatch++;
    bad.push([f, `${fmFaq.length} schema Qs vs ${vis.length} visible Qs`]);
    if (FIX) {
      // Rebuild the faq: block from the visible FAQ
      const faqYaml = 'faq:\n' + vis.map(x =>
        `  - question: ${yamlStr(x.question)}\n    answer: ${yamlStr(x.answer)}`
      ).join('\n');
      const newFm = fmRaw.replace(/^faq:\s*[\s\S]*?(?=^\S|\Z)/m, faqYaml + '\n');
      if (newFm === fmRaw) { stats.errors++; bad.push([f, 'faq block replace failed']); continue; }
      fs.writeFileSync(p, '---' + newFm + '---' + body, 'utf8');
      stats.fixed++;
    }
  } else {
    stats.match++;
  }
}

console.log(JSON.stringify(stats, null, 1));
console.log('\nMismatches / gaps:');
for (const [f, why] of bad) console.log(`  ${f.replace('.md', '')}: ${why}`);
