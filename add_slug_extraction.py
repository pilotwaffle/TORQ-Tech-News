#!/usr/bin/env python3
"""Add slug extraction to multi_source_aggregator.py"""
import re

# Read the file
with open('multi_source_aggregator.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add extract_slug helper method after _get_fallback_image
helper_method = '''
    def _extract_slug(self, url: str, title: str = "") -> str:
        """Extract slug from URL or generate from title"""
        import re

        # Try to extract from MIT Sloan URL
        if "sloanreview.mit.edu/article/" in url:
            match = re.search(r'/article/([^/]+)/?', url)
            if match:
                return match.group(1)

        # Try to extract from other URL patterns
        if "hackernews" in url or "ycombinator" in url:
            # For HN, use the ID
            match = re.search(r'id=(\\d+)', url)
            if match:
                return f"hn-{match.group(1)}"

        # Fallback: generate from title
        if title:
            slug = title.lower()
            slug = re.sub(r'[^a-z0-9\\s-]', '', slug)
            slug = re.sub(r'\\s+', '-', slug)
            slug = re.sub(r'^-+|-+$', '', slug)
            return slug[:50]

        return "article"
'''

# Find where to insert (after _get_fallback_image method)
insert_pos = content.find('    def extract_article_content(self, url')
if insert_pos == -1:
    print("ERROR: Could not find insertion point")
    exit(1)

# Insert the helper method
content = content[:insert_pos] + helper_method + '\n\n' + content[insert_pos:]

# Now update the MIT Sloan article creation to include slug
old_append = '''                    articles.append({
                        'title': title[:100],
                        'excerpt': "Business strategy insights from MIT Sloan School of Management",
                        'image': self._get_fallback_image(),
                        'category': "Leadership",
                        'author': "MIT Sloan Review",
                        'date': datetime.now().strftime("%B %d, %Y"),
                        'reading_time': random.randint(7, 12),
                        'link': link,
                        'source': 'MIT Sloan'
                    })'''

new_append = '''                    articles.append({
                        'title': title[:100],
                        'excerpt': "Business strategy insights from MIT Sloan School of Management",
                        'image': self._get_fallback_image(),
                        'category': "Leadership",
                        'author': "MIT Sloan Review",
                        'date': datetime.now().strftime("%B %d, %Y"),
                        'reading_time': random.randint(7, 12),
                        'link': link,
                        'slug': self._extract_slug(link, title),
                        'source': 'MIT Sloan'
                    })'''

content = content.replace(old_append, new_append)

# Also update Hacker News articles to include slug
hn_old = '''                'link': f"https://news.ycombinator.com/item?id={item.get('objectID', '')}",
                'source': 'Hacker News'
            })'''

hn_new = '''                'link': f"https://news.ycombinator.com/item?id={item.get('objectID', '')}",
                'slug': self._extract_slug(f"https://news.ycombinator.com/item?id={item.get('objectID', '')}", item.get('title', '')),
                'source': 'Hacker News'
            })'''

content = content.replace(hn_old, hn_new)

# Write the updated file
with open('multi_source_aggregator.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("[OK] Added slug extraction to multi_source_aggregator.py")
print("   - Added _extract_slug() helper method")
print("   - Updated MIT Sloan articles to include slug")
print("   - Updated Hacker News articles to include slug")
