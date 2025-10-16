# 🚀 Deploy TORQ Tech News - Step by Step

## ✅ Option 1: Deploy to Vercel (Easiest - via Dashboard)

### 1. Go to Vercel
Open: **https://vercel.com/new**

### 2. Import from GitHub
- Click "Import Git Repository"
- Search for: `TOTQ-Tech-News`
- Click "Import"

### 3. Configure Project
- **Framework Preset**: Other
- **Root Directory**: ./
- **Build Command**: (leave empty)
- **Output Directory**: (leave empty)
- **Install Command**: `pip install -r requirements.txt`

### 4. Deploy!
- Click "Deploy"
- Wait 2-3 minutes
- Get your URL: `https://torq-tech-news.vercel.app`

### 5. Verify
- Visit your URL
- Check homepage loads
- Scroll to see AI/ML section
- Click articles to test

### ⚠️ Important Note for Vercel
Vercel is **serverless**, so:
- ✅ Website works perfectly
- ✅ Cron jobs trigger at 6AM & 11PM (configured in vercel.json)
- ❌ SQLite database won't persist (need external DB)
- ❌ Background scheduler won't run continuously

**For true 24/7 automation, use Railway (Option 2) instead**

---

## 🏆 Option 2: Deploy to Railway (RECOMMENDED for 24/7)

### Why Railway?
- ✅ **24/7 operation** - background scheduler works
- ✅ **SQLite persists** - database stays between restarts
- ✅ **$5/month** after 500 free hours (or free forever under 500hrs)
- ✅ **Auto-deploys** from GitHub
- ✅ **Zero configuration** needed

### Step-by-Step:

#### 1. Go to Railway
Open: **https://railway.app/**

#### 2. Sign Up with GitHub
- Click "Login with GitHub"
- Authorize Railway
- Confirm email

#### 3. Create New Project
- Click "New Project"
- Select "Deploy from GitHub repo"
- Find: `TOTQ-Tech-News`
- Click on it

#### 4. Railway Auto-Configures
Railway automatically detects:
- ✅ Python runtime
- ✅ requirements.txt
- ✅ Start command: `python app.py`
- ✅ Port: 5000

**You don't need to change anything!**

#### 5. Deploy
- Click "Deploy"
- Wait 2-3 minutes
- Watch logs for:
  ```
  [AUTO] Content auto-update service started
  [AUTO] Scheduled updates: Daily at 6:00 AM and 11:00 PM
  ```

#### 6. Get Your URL
- Go to "Settings" tab
- Click "Generate Domain"
- Copy your URL: `https://torq-tech-news.up.railway.app`

#### 7. Verify 24/7 Operation
- Visit your URL
- Check logs: Should see scheduler running
- Database persists automatically
- Background automation active

#### 8. Monitor
- **Logs**: Railway Dashboard → Logs tab
- **Metrics**: See CPU, Memory, Network usage
- **Cost**: Track usage (500 hours free/month)

---

## 💻 Option 3: Deploy via Vercel CLI (Advanced)

If you want to deploy from terminal:

```bash
# 1. Navigate to project
cd E:\sloan-review-landing

# 2. Login to Vercel
vercel login

# 3. Deploy
vercel

# Follow prompts:
# - Set up and deploy? Yes
# - Which scope? [your account]
# - Link to existing project? No
# - What's your project's name? torq-tech-news
# - In which directory is your code located? ./
# - Want to override settings? No

# 4. Deploy to production
vercel --prod
```

---

## 🔧 After Deployment

### Test Manual Update Endpoint
```bash
# Visit in browser:
https://your-app.vercel.app/api/manual-update

# Should return:
{
  "status": "success",
  "message": "Content updated successfully",
  "timestamp": "2025-10-16T..."
}
```

### Test Admin Dashboard
```bash
# Visit:
https://your-app.vercel.app/admin

# See analytics dashboard
```

### Check Logs
**Vercel**: Dashboard → Your Project → Logs
**Railway**: Dashboard → Your Project → Logs

---

## 🎯 Which Should You Choose?

| Use Case | Choose |
|----------|--------|
| **Quick demo, testing** | Vercel (free, fast) |
| **Production, 24/7 automation** | Railway ($5/month) |
| **Need both speed + automation** | Railway + Vercel combo |
| **100% free requirement** | Vercel + GitHub Actions |

---

## 🚨 Current Status

✅ Code pushed to GitHub: `pilotwaffle/TOTQ-Tech-News`
✅ Vercel configuration complete
✅ Railway-ready (zero config needed)
✅ Cron jobs configured
✅ Manual update endpoint added

**Next**: Choose your deployment platform and follow the steps above!

---

## 📞 Need Help?

**Railway Issues**: https://help.railway.app/
**Vercel Issues**: https://vercel.com/support

**GitHub Repo**: https://github.com/pilotwaffle/TOTQ-Tech-News

---

## 🎉 Quick Links

**Vercel Deploy**: https://vercel.com/new
**Railway Deploy**: https://railway.app/new
**GitHub Repo**: https://github.com/pilotwaffle/TOTQ-Tech-News

---

**My Recommendation**: Use **Railway** for the best experience!
- One-click deployment
- 24/7 automation works perfectly
- SQLite database persists
- $5/month (or free under 500 hours)
- No configuration needed

**Deploy now**: https://railway.app/new
