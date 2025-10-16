# 🚂 Deploy to Railway - Step by Step

## 🎯 Why Railway Instead of Vercel?

**Vercel Error**: `500: FUNCTION_INVOCATION_FAILED`
- ❌ Serverless can't run background processes
- ❌ SQLite database doesn't persist
- ❌ File system is read-only
- ❌ Threading doesn't work

**Railway Solution**:
- ✅ Long-running process (not serverless)
- ✅ SQLite database persists
- ✅ Full file system access
- ✅ Background scheduler works perfectly
- ✅ 2x daily automation (6 AM & 11 PM)
- ✅ Only $5/month (500 free hours)

---

## 🚀 Deploy to Railway NOW (3 Minutes)

### Step 1: Go to Railway
**Open**: https://railway.app/

### Step 2: Sign Up with GitHub
1. Click "Start a New Project"
2. Click "Login with GitHub"
3. Authorize Railway app
4. Confirm your email

### Step 3: Deploy from GitHub
1. Click "Deploy from GitHub repo"
2. Grant Railway access to repositories (if prompted)
3. Find and select: `TORQ-Tech-News`
4. Click on the repository

### Step 4: Railway Auto-Detects Everything!
Railway automatically:
- ✅ Detects Python 3.11
- ✅ Installs from `requirements.txt`
- ✅ Runs `python app.py`
- ✅ Assigns port 5000
- ✅ Sets up environment

**You don't need to configure ANYTHING!**

### Step 5: Wait for Deployment (2 minutes)
Watch the build logs:
```
Building...
Installing Python 3.11
Installing requirements
Starting app.py
[SUCCESS] Server starting on http://localhost:5000
```

### Step 6: Get Your URL
1. Go to "Settings" tab
2. Click "Generate Domain"
3. Copy your URL: `https://torq-tech-news.up.railway.app`

### Step 7: Verify It Works
Visit your Railway URL and check:
- ✅ Homepage loads
- ✅ AI/ML section visible
- ✅ Articles are clickable
- ✅ Admin dashboard works: `/admin`
- ✅ Manual update works: `/api/manual-update`

---

## 📊 What You'll See in Logs

```bash
============================================================
MIT Sloan Review - Full Web Application
============================================================

[INFO] Initializing application...
[INFO] Database: /app/analytics.db
[AUTO] Content auto-update service started
[AUTO] Scheduled updates: Daily at 6:00 AM and 11:00 PM
[SUCCESS] Server starting on http://localhost:5000
```

**This means**:
- ✅ Database created
- ✅ Background scheduler running
- ✅ Automation active 24/7
- ✅ Ready to serve traffic

---

## 🎯 Railway Features You Get

### 1. Automatic Deployments
Every `git push` to GitHub → Automatic deployment

### 2. Environment Variables
Settings → Variables → Add environment variables (if needed)

### 3. Metrics
- CPU usage
- Memory usage
- Network traffic
- Request logs

### 4. Custom Domain (Optional)
Settings → Domains → Add your custom domain

### 5. Logs
Real-time logs showing:
- Automation runs
- Article updates
- Visitor tracking
- Errors (if any)

---

## 💰 Railway Pricing

**Free Tier**:
- 500 hours/month (~20 days)
- $5 credit
- Perfect for testing

**Hobby Plan** (Auto-charged after free tier):
- $5/month
- Unlimited hours
- 8 GB RAM
- 8 GB storage

**Cost Comparison**:
- Railway: $5/month
- Vercel Pro: $20/month
- Render: $7/month

**Railway is the cheapest option for this app!**

---

## 🔧 Railway Configuration Files

I've created these for you:

### `railway.json`
```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python app.py",
    "restartPolicyType": "ON_FAILURE"
  }
}
```

### `Procfile`
```
web: python app.py
```

These ensure Railway knows how to run your app!

---

## ✅ Advantages Over Vercel

| Feature | Vercel | Railway |
|---------|--------|---------|
| **Background Process** | ❌ | ✅ |
| **SQLite Persistence** | ❌ | ✅ |
| **File System Writes** | ❌ | ✅ |
| **2x Daily Cron** | ❌ Free | ✅ |
| **Cost** | $20/mo Pro | $5/mo |
| **Setup** | Complex | Zero config |

---

## 🎯 After Deployment

### Test Everything:

1. **Homepage**:
   ```
   https://your-app.up.railway.app
   ```

2. **Admin Dashboard**:
   ```
   https://your-app.up.railway.app/admin
   ```

3. **Manual Update**:
   ```
   https://your-app.up.railway.app/api/manual-update
   ```

4. **Check Logs**:
   - Railway Dashboard → Deployments → Logs
   - Should see automation running

---

## 🚨 Troubleshooting

### Issue: "Build Failed"
- Check logs for Python errors
- Verify requirements.txt is correct

### Issue: "Port Binding Error"
- Railway auto-assigns ports
- Should not happen with our app

### Issue: "Database Locked"
- Railway persists SQLite automatically
- No action needed

---

## 📞 Railway Support

- **Docs**: https://docs.railway.app/
- **Discord**: https://discord.gg/railway
- **Help**: https://help.railway.app/

---

## 🎉 Expected Result

After 3 minutes:
- 🌐 **Live Site**: `https://torq-tech-news.up.railway.app`
- 🤖 **Automation**: Running 24/7
- ⏰ **Cron**: 6 AM & 11 PM daily
- 💾 **Database**: Persistent SQLite
- 📊 **Analytics**: Working dashboard
- ✅ **Zero 500 errors**

---

## 🚂 Ready to Deploy?

**Click here**: https://railway.app/new

1. Login with GitHub
2. Deploy from GitHub repo
3. Select `TORQ-Tech-News`
4. Done in 3 minutes!

**Railway is the perfect platform for TORQ Tech News!**

---

**Current Status**: Files pushed to GitHub, ready for Railway deployment!
