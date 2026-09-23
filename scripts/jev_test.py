#!/usr/bin/env python3
"""Test JEV on 5 top TradieAutomate pages — intent classification + meta diagnosis."""
import json, os, sys
sys.path.insert(0, os.path.expanduser('/Users/shane/tradieautomate/repo/scripts'))
from jev_classify import jev_classify

# Load dashboard for top pages by impression
d = json.load(open(os.path.expanduser('~/tradieautomate/dashboard.json')))
pages = d.get('gsc', {}).get('pages', [])[:5]

# Read actual title/description for each
repo = os.path.expanduser('/Users/shane/tradieautomate/repo')
page_data = []
for p in pages:
    slug = p['slug']
    fpath = f'{repo}/src/content/blog/{slug}.md'
    if not os.path.exists(fpath):
        continue
    content = open(fpath).read()
    title = ''
    desc = ''
    for line in content.splitlines():
        if line.startswith('title:'):
            title = line.split(':', 1)[1].strip().strip("'\"").strip()
        if line.startswith('description:'):
            desc = line.split(':', 1)[1].strip().strip("'\"").strip()
    page_data.append({
        'slug': slug,
        'impressions': p.get('impressions', 0),
        'ctr': p.get('ctr', 0),
        'position': p.get('position', 0),
        'title': title,
        'description': desc
    })

# Classify each — batch one question per page to avoid rate limits
print(f'Testing {len(page_data)} pages...')
for pg in page_data:
    state = f"Page title: {pg['title']}. Page description: {pg['description']}"
    result = jev_classify(state, {
        'intent': {
            'type': 'choice',
            'instructions': 'What search intent does this page target?',
            'criteria': {
                'lookup': 'Reader wants specific data, rates, steps, or how-to instructions',
                'compliance': 'Reader needs to understand a legal requirement, deadline, or penalty',
                'comparison': 'Reader is choosing between products, tools, or services',
                'strategy': 'Reader wants business growth advice or operational tips'
            }
        },
        'meta_quality': {
            'type': 'score',
            'instructions': 'How well does the meta lead with the data/differentiator/deliverable vs fear/feature?',
            'criteria': ['Poor', 'Below average', 'Average', 'Good', 'Excellent']
        },
        'has_stakes': {
            'type': 'boolean',
            'instructions': 'Does the description include a dollar figure, specific deadline, or concrete number?'
        }
    }, timeout=20)
    
    intent = result.get('intent', {}).get('choice', '?')
    prob = result.get('intent', {}).get('probabilities', {})
    quality = result.get('meta_quality', {}).get('score', 0)
    stakes = result.get('has_stakes', {}).get('choice', '?')
    
    print(f"\n{pg['slug']}")
    print(f"  imp={pg['impressions']}, ctr={pg['ctr']}%, pos={pg['position']}")
    print(f"  intent={intent} ({json.dumps(prob)}) | meta_quality={quality}/4 | stakes={stakes}")