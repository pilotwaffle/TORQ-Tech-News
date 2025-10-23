"""
Fix article slugs in data_cache.json
Adds slug fields to all articles based on their titles or links
"""
import json
import re
from datetime import datetime

def create_slug(title, link=""):
    """Generate URL-friendly slug from title or link"""
    # Try to extract slug from MIT Sloan Review link first
    if link and "sloanreview.mit.edu/article/" in link:
        # Extract slug from URL
        match = re.search(r'/article/([^/]+)/?$', link)
        if match:
            return match.group(1)
    
    # Otherwise generate from title
    slug = title.lower()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'\s+', '-', slug)
    slug = re.sub(r'^-+|-+$', '', slug)  # Remove leading/trailing dashes
    slug = slug[:50]  # Limit length
    return slug

# Load existing cache
with open('data_cache.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Add slugs to all articles
for article in data.get('articles', []):
    if 'slug' not in article or not article['slug']:
        article['slug'] = create_slug(article['title'], article.get('link', ''))
        print(f"Added slug '{article['slug']}' for: {article['title']}")

for article in data.get('ai_ml_articles', []):
    if 'slug' not in article or not article['slug']:
        article['slug'] = create_slug(article['title'], article.get('link', ''))
        print(f"Added AI/ML slug '{article['slug']}' for: {article['title']}")

# Update timestamp
data['timestamp'] = datetime.now().isoformat()

# Save updated cache
with open('data_cache.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("\n✅ Successfully added slugs to all articles!")
print(f"Updated {len(data.get('articles', []))} main articles")
print(f"Updated {len(data.get('ai_ml_articles', []))} AI/ML articles")
