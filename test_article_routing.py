#!/usr/bin/env python3
"""Test article routing fix"""
import json
import re

def normalize_slug(title):
    slug = title.lower()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'\s+', '-', slug)
    slug = re.sub(r'^-+|-+$', '', slug)
    return slug[:50]

with open('data_cache.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    articles = data.get('articles', [])

print('Testing all 6 articles:')
print('=' * 60)

for i, article in enumerate(articles, 1):
    title = article['title']
    slug = article.get('slug', 'NO SLUG')
    normalized = normalize_slug(title)

    print(f'\n{i}. {title}')
    print(f'   Slug field: {slug}')
    print(f'   Normalized: {normalized}')
    if slug != normalized:
        print('   Result: DIFFERENT - Fix needed and applied')
    else:
        print('   Result: SAME - Would work either way')

print('\n' + '=' * 60)
print('Testing specific slug from error:')
test_slug = 'whats-your-edge-rethinking-expertise-in-the-age-of-ai'
old_match = next((a for a in articles if normalize_slug(a['title']) == test_slug), None)
new_match = next((a for a in articles if a.get('slug') == test_slug), None)

print(f'\nSlug to match: {test_slug}')
print(f'OLD WAY (normalize title): Found = {old_match is not None}')
print(f'NEW WAY (slug field): Found = {new_match is not None}')

if new_match:
    print(f'\nMatched article:')
    print(f'  Title: {new_match["title"]}')
    print(f'  Author: {new_match["author"]}')
    print(f'  Link: {new_match["link"]}')
