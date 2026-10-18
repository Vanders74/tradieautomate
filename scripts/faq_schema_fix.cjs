#!/usr/bin/env node
/**
 * faq_schema_fix.cjs — make JSON-LD FAQ schema match the visible FAQ.
 *
 * Three defects, one sweep:
 *   1. mismatch          -> rewrite frontmatter `faq:` to mirror the visible FAQ
 *   2. visibleNoSchema   -> add `faq:` frontmatter parsed from the visible FAQ
 *   3. schemaNoVisible   -> append a visible "Frequently Asked Questions"
 *                           section built from the frontmatter `faq:`
 *
 * Visible content is ground truth (Google requires schema to reflect what the
 * user can see). Frontmatter is edited textually — only the faq block — so
 * dates and quoting elsewhere are never reformatted.
 *
 * Usage: node scripts/faq_schema_fix.cjs [--dry-run] [--only slug]
 */
const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');

const BLOG = path.join(__dirname, '..', 'src', 'content', 'blog');
const DRY = process.argv.includes('--dry-run');
const onlyIdx = process.argv.indexOf('--only');
const ONLY = onlyIdx > -1 ? process.argv[onlyIdx + 1] : null;

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
    if (/^##\s+.*(frequently asked questions|\bFAQ\b|common questions)\s*(\([^)]*\))?\s*$/i.test(ln)) { inFaq = true; continue; }
    if (inFaq && /^##\s+/.test(ln)) { flush(); break; }
    if (!inFaq) continue;
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
const yamlStr = s => '"' + String(s).replace(/\\/g, '\\\\').replace(/"/g, '\\"').replace(/\n/g, ' ') + '"';

function faqBlock(items) {
  return 'faq:\n' + items.map(x =>
    `  - question: ${yamlStr(x.question)}\n    answer: ${yamlStr(x.answer)}`
  ).join('\n');
}

/** Replace the top-level `faq:` block (or insert one) in frontmatter text. */
function setFaqBlock(fmRaw, block) {
  const lines = fmRaw.split('\n');
  const start = lines.findIndex(l => /^faq:\s*$/.test(l));
  if (start > -1) {
    let end = lines.length;
    for (let i = start + 1; i < lines.length; i++) {
      if (/^[A-Za-z_][\w-]*:/.test(lines[i])) { end = i; break; }
    }
    const before = lines.slice(0, start);
    const after = lines.slice(end);
    return [...before, ...block.split('\n'), ...after].join('\n');
  }
  // insert after description: line if present, else at end
  const di = lines.findIndex(l => /^description:/.test(l));
  const at = di > -1 ? di + 1 : lines.length;
  return [...lines.slice(0, at), ...block.split('\n'), ...lines.slice(at)].join('\n');
}

function appendVisibleFaq(body, items) {
  const section = '\n## Frequently Asked Questions\n\n' +
    items.map(x => `### ${x.question}\n\n${x.answer}`).join('\n\n') + '\n';
  const rel = body.search(/^##\s+Related Reading/m);
  if (rel > -1) return body.slice(0, rel) + section + '\n' + body.slice(rel);
  return body.replace(/\s*$/, '\n') + section;
}

let stats = { total: 0, mismatch: 0, visibleNoSchema: 0, schemaNoVisible: 0, unchanged: 0, written: 0, errors: [] };
const files = fs.readdirSync(BLOG).filter(f => f.endsWith('.md'));

for (const f of files) {
  if (ONLY && !f.startsWith(ONLY)) continue;
  stats.total++;
  const p = path.join(BLOG, f);
  const txt = fs.readFileSync(p, 'utf8');
  const [fmRaw, body] = splitFm(txt);
  if (fmRaw === null) continue;

  let data;
  try { data = yaml.load(fmRaw) || {}; } catch (e) { stats.errors.push([f, 'yaml']); continue; }
  const fmFaq = Array.isArray(data.faq) ? data.faq.filter(x => x && x.question && x.answer) : [];
  const vis = visibleFaq(body);

  let newFm = fmRaw, newBody = body, kind = null;

  if (vis.length && fmFaq.length) {
    const fmMap = new Map(fmFaq.map(x => [norm(x.question), norm(x.answer)]));
    const visMap = new Map(vis.map(x => [norm(x.question), norm(x.answer)]));
    let mismatch = fmMap.size !== visMap.size;
    if (!mismatch) for (const [q, a] of visMap) {
      if (!fmMap.has(q) || fmMap.get(q).slice(0, 100) !== a.slice(0, 100)) { mismatch = true; break; }
    }
    if (mismatch) { newFm = setFaqBlock(fmRaw, faqBlock(vis)); kind = 'mismatch'; }
  } else if (vis.length && !fmFaq.length) {
    newFm = setFaqBlock(fmRaw, faqBlock(vis));
    kind = 'visibleNoSchema';
  } else if (!vis.length && fmFaq.length) {
    newBody = appendVisibleFaq(body, fmFaq);
    kind = 'schemaNoVisible';
  }

  if (!kind) { stats.unchanged++; continue; }
  stats[kind]++;

  // sanity: the edited frontmatter must still parse
  try { yaml.load(newFm); } catch (e) { stats.errors.push([f, 'edited yaml invalid']); continue; }

  if (!DRY) {
    const out = '---' + (newFm.startsWith('\n') ? newFm : '\n' + newFm) + '\n---' + newBody;
    // validate the reconstructed document before writing
    try { const [c] = splitFm(out); yaml.load(c); } catch (e) { stats.errors.push([f, 'reconstructed invalid']); continue; }
    fs.writeFileSync(p, out, 'utf8');
    stats.written++;
  }
}

console.log(JSON.stringify({ ...stats, errors: stats.errors.length }, null, 1));
for (const [f, why] of stats.errors) console.log(`  ERROR ${f}: ${why}`);
