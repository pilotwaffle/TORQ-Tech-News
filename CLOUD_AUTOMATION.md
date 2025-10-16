# TORQ Tech News - 24/7 Cloud Automation Guide

## 🎯 Problem: Vercel Serverless Limitations

Vercel is **serverless**, which means:
- ❌ No long-running background processes
- ❌ The `schedule` library won't work
- ❌ Functions timeout after 10 seconds (free) / 60 seconds (pro)
- ✅ But Vercel Cron Jobs CAN trigger updates at 6AM & 11PM

## ✅ Solution: Hybrid Approach

### Option 1: Vercel + Vercel Cron Jobs (RECOMMENDED FOR SIMPLICITY)
**Best for**: Low-maintenance, serverless-first approach

**Pros**:
- Free tier includes cron jobs
- No server management
- Auto-scaling
- Edge network (fast globally)

**Cons**:
- Cron limited to once per hour minimum on free tier
- Database (SQLite) won't persist between invocations
- Need to use external storage (Vercel KV, PostgreSQL, etc.)

**Setup**:
1. Deploy to Vercel (done via `vercel.json`)
2. Cron automatically triggers `/api/cron/update-content` at 6AM & 11PM
3. Use Vercel KV or PostgreSQL for persistent storage

---

### Option 2: Railway.app (RECOMMENDED FOR TRUE 24/7 OPERATION)
**Best for**: Long-running processes, background tasks, SQLite database

**Pros**:
- ✅ Supports long-running processes
- ✅ SQLite database persists
- ✅ Background scheduler works perfectly
- ✅ $5/month free tier (500 hours)
- ✅ Auto-deploys from GitHub
- ✅ Zero configuration needed

**Cons**:
- Costs $5/month after free tier
- Single server (no auto-scaling)

**Setup Instructions**:

1. **Go to Railway.app**
   ```
   https://railway.app/
   ```

2. **Sign up with GitHub**
   - Click "Login with GitHub"
   - Authorize Railway

3. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose `pilotwaffle/TOTQ-Tech-News`

4. **Configure Settings**
   - Railway auto-detects Python
   - No configuration needed!
   - Start command: `python app.py`

5. **Deploy**
   - Click "Deploy"
   - Wait 2-3 minutes
   - Get your live URL: `https://your-app.railway.app`

6. **Verify Automation**
   - Check logs: "Scheduled updates: Daily at 6:00 AM and 11:00 PM"
   - The background scheduler runs automatically
   - SQLite database persists

**Cost**:
- Free tier: 500 hours/month (enough for 24/7)
- After free tier: ~$5/month

---

### Option 3: Render.com (ALTERNATIVE TO RAILWAY)
**Best for**: Free tier, similar to Railway

**Pros**:
- ✅ Free tier available
- ✅ Supports long-running processes
- ✅ Auto-deploys from GitHub
- ✅ Similar to Railway

**Cons**:
- Free tier sleeps after inactivity
- Need $7/month for 24/7 operation

**Setup**:
1. Go to https://render.com/
2. Sign up with GitHub
3. New Web Service → Connect `TOTQ-Tech-News`
4. Settings:
   - Runtime: Python 3
   - Build: `pip install -r requirements.txt`
   - Start: `python app.py`
5. Deploy

---

### Option 4: GitHub Actions (FOR CONTENT UPDATES ONLY)
**Best for**: Triggering content updates, not hosting the site

**Pros**:
- ✅ Completely free
- ✅ Runs on schedule
- ✅ No server needed

**Cons**:
- ❌ Can't host the website
- ❌ Only for automation tasks

**Setup**:

Create `.github/workflows/update-content.yml`:

```yaml
name: Update Content

on:
  schedule:
    # Run at 6:00 AM UTC (adjust timezone as needed)
    - cron: '0 6 * * *'
    # Run at 11:00 PM UTC
    - cron: '0 23 * * *'
  workflow_dispatch: # Allow manual trigger

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt

      - name: Run automation agent
        run: |
          python automation_agent.py

      - name: Commit and push changes
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add .
          git commit -m "chore: Automated content update" || echo "No changes"
          git push
```

**Use Case**: Update content files, push to GitHub, Vercel auto-deploys

---

## 🏆 RECOMMENDED SOLUTION: Railway + Vercel

### Why This Combo?

1. **Railway** ($5/month): Runs the automation 24/7
   - Background scheduler works
   - SQLite persists
   - Handles cron jobs at 6AM & 11PM

2. **Vercel** (Free): Serves the website
   - Fast edge network
   - Auto-scaling
   - Free SSL
   - Custom domain support

### Setup Steps:

#### Step 1: Deploy to Railway (Automation)
```bash
1. Go to https://railway.app/
2. New Project → Deploy from GitHub
3. Select: pilotwaffle/TOTQ-Tech-News
4. Wait for deployment
5. Get URL: https://your-app.railway.app
```

#### Step 2: Deploy to Vercel (Website)
```bash
1. Go to https://vercel.com/new
2. Import: pilotwaffle/TOTQ-Tech-News
3. Click Deploy
4. Get URL: https://torq-tech-news.vercel.app
```

#### Step 3: Point Vercel to Railway Data
Modify Vercel deployment to fetch content from Railway:

```python
# In app.py, add environment variable for Railway URL
RAILWAY_API_URL = os.getenv('RAILWAY_API_URL', 'http://localhost:5000')

@app.route('/')
def home():
    # Fetch content from Railway if in production
    if RAILWAY_API_URL != 'http://localhost:5000':
        response = requests.get(f'{RAILWAY_API_URL}/api/content')
        content = response.json()
    # ... rest of code
```

---

## 💰 Cost Comparison

| Solution | Monthly Cost | Pros | Cons |
|----------|-------------|------|------|
| **Vercel Only** | $0 | Free, fast | No background tasks |
| **Railway** | $5 | 24/7, SQLite works | Single server |
| **Render** | $7 | 24/7, auto-scale | More expensive |
| **GitHub Actions** | $0 | Free | Can't host site |
| **Railway + Vercel** | $5 | Best of both | Slightly complex |

---

## 🚀 Quick Deploy to Railway NOW

1. **Open Railway**: https://railway.app/new
2. **Login with GitHub**
3. **Deploy from GitHub**: `pilotwaffle/TOTQ-Tech-News`
4. **Done!** - Your site is live with 24/7 automation

---

## 🎯 My Recommendation

**For You**: Use **Railway.app** ($5/month)

**Why**:
- ✅ Zero configuration needed
- ✅ Auto-deploys from your GitHub repo
- ✅ Background scheduler works perfectly
- ✅ SQLite database persists
- ✅ 24/7 operation guaranteed
- ✅ Logs available for debugging
- ✅ Custom domain support
- ✅ SSL included
- ✅ Can scale if needed

**Alternative**: If you want 100% free, use:
- Vercel (website hosting) + GitHub Actions (content updates)
- Content updates commit to GitHub → Vercel auto-deploys

---

## 📝 Updated Vercel Configuration

I've already updated your `vercel.json` to include Vercel Cron Jobs:

```json
{
  "crons": [
    {
      "path": "/api/cron/update-content",
      "schedule": "0 6,23 * * *"
    }
  ]
}
```

This will work on Vercel, but remember:
- Vercel Cron needs Pro plan for custom schedules
- Free tier limited to once per hour minimum
- No persistent SQLite

---

## 🔧 Testing the Cron Endpoint

After deployment, test manually:

```bash
# Visit in browser or curl
https://your-app.vercel.app/api/manual-update

# Should return:
{
  "status": "success",
  "message": "Content updated successfully",
  "timestamp": "2025-10-16T..."
}
```

---

## 📊 Monitoring

### Railway Logs
```
Railway Dashboard → Your Project → Logs
```

### Vercel Logs
```
Vercel Dashboard → Your Project → Logs
```

### Manual Trigger
```
Visit: https://your-app/api/manual-update
```

---

**Recommendation**: Deploy to Railway now, it's the easiest and most reliable solution for 24/7 operation!
