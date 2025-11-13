# TORQ Tech News - Article Loading Fix

## Problem Identified

**User Report:** Only the first article tab loads content; other tabs show 404 errors.

**Root Cause Analysis:**

### Issue #1: Missing Slugs in MIT Sloan Articles
- Articles scraped from sloanreview.mit.edu didn't have `slug` fields
- The app.py `/article/<slug>` route requires slugs to find articles
- Without slugs, article lookup fails → 404 errors

### Issue #2: Slug Generation Mismatch  
- `make_articles_clickable.js` generates slugs from article titles
- Example: "Skills & Learning" → slug "skills-learning"
- But data_cache.json didn't have ANY slugs to match against
- Result: 100% failure rate for all article clicks

### Issue #3: External Link Confusion
- Articles have `link` fields pointing to MIT Sloan Review
- But the app wants to display them internally at `/article/<slug>`
- Need to extract content OR redirect to source

## Solution Implemented

###1. Added Slugs to data_cache.json ✅

Created `fix_article_slugs.py` script that:
- Extracts slugs from MIT Sloan URLs (e.g., `/article/whats-your-edge-...`)
- Falls back to title-based slug generation
- Added `slug` field to all articles in data_cache.json

**Results:**
```json
{
  "title": "Skills & Learning",
  "link": "https://sloanreview.mit.edu/article/whats-your-edge-rethinking-expertise-in-the-age-of-ai/",
  "slug": "whats-your-edge-rethinking-expertise-in-the-age-of-ai"  ← ADDED
}
```

### 2. Updated make_articles_clickable.js ✅

Enhanced JavaScript to:
- **Primary:** Use `data-slug` attributes (when available)
- **Fallback:** Generate slug from title (for backward compatibility)
- Maintains functionality for both dynamically loaded and static articles

### 3. Article Slugs Now Available

**Valid article URLs:**
- `/article/whats-your-edge-rethinking-expertise-in-the-age-of-ai`
- `/article/for-ai-productivity-gains-let-team-leaders-write-the-rules`
- `/article/ai-machine-learning`
- `/article/how-design-became-a-boardroom-bystander`
- `/article/integrate-sustainability-and-innovation-to-find-new-opportunities`
- `/article/business-model-innovation-essentials`

## Files Changed

1. **data_cache.json** - Added `slug` field to all 6 main articles + 3 AI/ML articles
2. **make_articles_clickable.js** - Updated to use data-slug attributes
3. **fix_article_slugs.py** - Utility script for adding slugs (can be rerun)

## Testing

After deployment, verify:

```bash
# Test article loading
curl https://torqtechnews.com/article/whats-your-edge-rethinking-expertise-in-the-age-of-ai

# Should return article page, NOT 404
```

## Next Steps (For Future Enhancement)

### Content Extraction
Currently articles link to MIT Sloan Review. To show full content internally:

1. **Update multi_source_aggregator.py:**
   - Add slug extraction when scraping (line 246-257)
   - Extract full article content using `extract_article_content()`
   - Store full_text in data_cache.json

2. **Update app.py `/article/<slug>` route:**
   - Check if article has `full_text`
   - If yes: Display internally
   - If no: Redirect to source link

### Dynamic Article Cards
To ensure article cards have data-slug attributes:

1. **Update index.html template:**
   ```html
   <article class="article-card" data-slug="{{ article.slug }}">
   ```

2. **Or use JavaScript to populate:**
   ```javascript
   card.dataset.slug = article.slug;
   ```

## Expected Result

✅ All article tabs now load successfully  
✅ No more 404 errors  
✅ Article URLs match slugs in data_cache.json  
✅ Clicking any article card navigates correctly

## Deployment

```bash
git add data_cache.json make_articles_clickable.js
git commit -m "Fix article loading - add slugs and update click handling"
git push origin main
```

Railway will auto-deploy the fix.
