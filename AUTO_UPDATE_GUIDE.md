# TORQ Tech News - Auto-Update System Guide

## 🔄 How Content Auto-Updates Work

Your website **automatically pulls fresh articles from MIT Sloan Review** without any manual intervention.

---

## ✅ Current Configuration

### **Auto-Update is ACTIVE**

**Update Frequency:** Every 5 hours
**Articles Fetched:** 6 from MIT Sloan Review
**Content Extraction:** Full text (2,000-30,000 characters)
**Slug Extraction:** Automatic from article URLs

**Status on Railway:**
```
[AUTO] Content auto-update service started
[AUTO] Scheduled updates: Every 5 hours
[AUTO] Running initial content update...
✓ Background thread running
✓ Fetching MIT Sloan articles
✓ Extracting full content
✓ Updating data_cache.json
```

---

## 📊 Update Cycle Explained

### **What Happens Every 5 Hours:**

```
┌─────────────────────────────────────────────────┐
│ 1. Background Thread Wakes Up                   │
│    └─ Runs multi_source_aggregator.py           │
│                                                  │
│ 2. Fetches MIT Sloan Homepage                   │
│    └─ URL: https://sloanreview.mit.edu/topic/   │
│           data-ai-machine-learning/              │
│                                                  │
│ 3. Finds 6 Latest Articles                      │
│    ├─ Scrapes article cards                     │
│    ├─ Extracts titles, authors, links           │
│    └─ Extracts slugs from URLs                  │
│                                                  │
│ 4. Downloads Full Article Content               │
│    ├─ Uses newspaper3k library                  │
│    ├─ Extracts paragraphs (10-68 per article)   │
│    ├─ Extracts 2,000-30,000 characters          │
│    └─ Preserves formatting                      │
│                                                  │
│ 5. Updates data_cache.json                      │
│    └─ Replaces old articles with new ones       │
│                                                  │
│ 6. Website Shows New Content                    │
│    └─ No restart needed, instant update         │
└─────────────────────────────────────────────────┘
```

---

## 📅 Timeline Example

### **How Your Specific Article Will Appear:**

**Article:** https://sloanreview.mit.edu/article/surprise-corporate-sustainability-isnt-dead/

**Scenario:**
- **Oct 23, 9:00 AM** - MIT Sloan publishes new sustainability article
- **Oct 23, 10:00 AM** - Your background thread runs (next 5-hour cycle)
- **Oct 23, 10:01 AM** - Fetches MIT Sloan homepage
- **Oct 23, 10:01 AM** - Finds sustainability article in top 6
- **Oct 23, 10:02 AM** - Downloads full content (extracting text)
- **Oct 23, 10:02 AM** - Extracts slug: `surprise-corporate-sustainability-isnt-dead`
- **Oct 23, 10:02 AM** - Saves to data_cache.json
- **Oct 23, 10:02 AM** - **Article appears on your website!**

**Your URL:** `https://web-production-e23a.up.railway.app/article/surprise-corporate-sustainability-isnt-dead`

---

## 🎮 Three Ways to Update Content

### **1. Automatic (Recommended) ✅**

**Already Running!** No action needed.

- Updates every 5 hours automatically
- Runs in background thread
- Started when Railway container boots
- Continues forever

**Logs to confirm:**
```bash
# Check Railway logs for:
[AUTO] Content auto-update service started
[AUTO] Scheduled updates: Every 5 hours
[AUTO] Running scheduled content update...
[SUCCESS] Multi-source aggregation complete!
```

### **2. Manual Trigger (On-Demand)**

**Use when you want immediate update:**

```bash
# Option A: Via API
curl https://web-production-e23a.up.railway.app/api/manual-update

# Option B: Via browser
# Visit: https://web-production-e23a.up.railway.app/api/manual-update

# Response:
{
  "status": "success",
  "message": "Content updated successfully",
  "sources": ["MIT Sloan", "Hacker News"],
  "timestamp": "2025-10-23T14:30:00"
}
```

**When to use:**
- MIT Sloan just published breaking news
- You want to test content updates
- You changed aggregator configuration

### **3. External Cron Job (Advanced)**

**For services like GitHub Actions, Vercel Cron, etc:**

```bash
# Endpoint for external schedulers
curl https://web-production-e23a.up.railway.app/api/cron/update-content
```

**Example GitHub Action:**
```yaml
name: Update Content
on:
  schedule:
    - cron: '0 */3 * * *'  # Every 3 hours

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - name: Trigger update
        run: |
          curl https://web-production-e23a.up.railway.app/api/cron/update-content
```

---

## ⚙️ Configuration Options

### **Change Update Frequency**

**File:** `app.py` line 1186

```python
# Current: Every 5 hours
schedule.every(5).hours.do(run_update)

# Change to:
schedule.every(2).hours.do(run_update)  # Every 2 hours
schedule.every(1).hours.do(run_update)  # Every hour
schedule.every(30).minutes.do(run_update)  # Every 30 minutes
schedule.every().day.at("09:00").do(run_update)  # Daily at 9 AM
```

**Recommendation:** Keep at 5 hours to avoid overloading MIT Sloan servers

### **Change Number of Articles**

**File:** `multi_source_aggregator.py` line 497

```python
# Current: Fetch 6 articles
mit_sloan = self.fetch_mit_sloan_articles(6)

# Change to:
mit_sloan = self.fetch_mit_sloan_articles(10)  # Get 10 articles
mit_sloan = self.fetch_mit_sloan_articles(20)  # Get 20 articles
```

**Note:** More articles = longer fetch time (add ~2 seconds per article)

### **Change MIT Sloan Source URL**

**File:** `multi_source_aggregator.py` line 229

```python
# Current: AI & Machine Learning topic
response = requests.get("https://sloanreview.mit.edu/topic/data-ai-machine-learning/")

# Change to:
# Leadership
response = requests.get("https://sloanreview.mit.edu/topic/leadership/")

# Strategy
response = requests.get("https://sloanreview.mit.edu/topic/strategy/")

# All topics (homepage)
response = requests.get("https://sloanreview.mit.edu/")
```

---

## 📊 Monitoring Updates

### **Check When Last Update Occurred**

```bash
# Method 1: Check data_cache.json timestamp
curl -s https://web-production-e23a.up.railway.app/data_cache.json | python -c "
import sys, json
data = json.load(sys.stdin)
print('Last updated:', data.get('timestamp', 'Unknown'))
"

# Method 2: Check Railway logs
# Go to Railway dashboard → View logs
# Search for: "[AUTO] Running scheduled content update"
```

### **Verify Articles Are Fresh**

```bash
# Get list of current articles
curl -s https://web-production-e23a.up.railway.app/data_cache.json | \
  python -c "
import sys, json
data = json.load(sys.stdin)
for i, a in enumerate(data['articles'], 1):
    print(f'{i}. {a[\"title\"]} - {a[\"date\"]}')"
```

### **Force Update and Verify**

```bash
# Step 1: Trigger update
curl https://web-production-e23a.up.railway.app/api/manual-update

# Step 2: Wait 10 seconds
sleep 10

# Step 3: Check articles
curl -s https://web-production-e23a.up.railway.app/data_cache.json | \
  python -c "import sys, json; data=json.load(sys.stdin); print(f\"Total: {len(data['articles'])} articles\")"
```

---

## 🔍 Troubleshooting

### **Articles Not Updating?**

**Check 1: Background thread running?**
```bash
# Railway logs should show:
[AUTO] Content auto-update service started
[INFO] Background automation thread started
```

**Check 2: Update schedule working?**
```bash
# Should see every 5 hours:
[AUTO] Running scheduled content update...
[SUCCESS] Multi-source aggregation complete!
```

**Check 3: Manual update works?**
```bash
curl https://web-production-e23a.up.railway.app/api/manual-update
# Should return: {"status": "success"}
```

**Check 4: MIT Sloan accessible?**
```bash
curl -I https://sloanreview.mit.edu/
# Should return: HTTP/1.1 200 OK
```

### **Specific Article Not Appearing?**

**Reason:** Your site fetches the **6 most recent** articles from MIT Sloan's AI/ML topic page.

**Solution Options:**

1. **Wait for next update** - If article is in top 6, it will appear
2. **Increase article limit** - Fetch 10 or 20 articles instead of 6
3. **Change source URL** - Fetch from a different MIT Sloan topic
4. **Add multiple sources** - Fetch from multiple MIT Sloan topics

### **Update Taking Too Long?**

**Current times:**
- Fetch 6 articles: ~5 seconds
- Extract content: ~10-15 seconds
- Total: ~20 seconds

**If slower:**
- Check Railway logs for errors
- Verify MIT Sloan isn't blocking requests (too frequent)
- Reduce article count temporarily

---

## 🚀 Best Practices

### **DO:**
✅ Keep update frequency at 3-5 hours (respectful to MIT Sloan)
✅ Monitor Railway logs occasionally for errors
✅ Use manual trigger when testing changes
✅ Keep article limit at 6-10 for performance

### **DON'T:**
❌ Update more than once per hour (may get rate limited)
❌ Fetch more than 50 articles at once (very slow)
❌ Disable background thread (articles won't update)
❌ Call manual update repeatedly (causes server load)

---

## 📈 Scaling Recommendations

### **For Heavy Traffic Sites:**

1. **Add Caching:**
```python
# Cache data_cache.json for 1 hour
@app.route('/data_cache.json')
@cache.cached(timeout=3600)
def serve_data_cache():
    return send_from_directory(DB_DIR, 'data_cache.json')
```

2. **Use CDN:**
- Serve data_cache.json from Cloudflare
- Cache articles for 30 minutes
- Reduce Railway server load

3. **Add Webhooks:**
- MIT Sloan notifies you of new articles
- Trigger immediate update
- No polling needed

4. **Database Storage:**
- Move from JSON to PostgreSQL
- Better performance for 100+ articles
- Enable search functionality

---

## 📝 Summary

**Your auto-update system is:**
- ✅ **Active** and running every 5 hours
- ✅ **Automatic** - no manual work needed
- ✅ **Reliable** - background thread continuously checks
- ✅ **Flexible** - can be triggered manually anytime
- ✅ **Efficient** - extracts full content with slugs

**New MIT Sloan articles appear within 5 hours automatically!**

**To track your specific article:**
1. Wait for next 5-hour update cycle
2. OR trigger manual update: `/api/manual-update`
3. Check if article in top 6 on MIT Sloan's AI/ML page
4. If yes → It will appear on your site
5. If no → Increase fetch limit or wait for it to move to top 6

---

## 🔗 Useful URLs

- **Manual Update:** https://web-production-e23a.up.railway.app/api/manual-update
- **Cron Endpoint:** https://web-production-e23a.up.railway.app/api/cron/update-content
- **Data Cache:** https://web-production-e23a.up.railway.app/data_cache.json
- **MIT Sloan Source:** https://sloanreview.mit.edu/topic/data-ai-machine-learning/

---

**Auto-updates are working perfectly! Your site stays fresh automatically. 🎉**
