# Deploying Private GitHub Repository to Vercel

## 🔐 Your Situation
- Repository: `TORQ-Tech-News` (PRIVATE)
- GitHub: https://github.com/pilotwaffle/TORQ-Tech-News
- Goal: Deploy to Vercel while keeping repository private

---

## ✅ Step-by-Step: Deploy Private Repo to Vercel

### Step 1: Grant Vercel Access to Private Repos

1. **Go to Vercel Dashboard**:
   - Visit: https://vercel.com/dashboard

2. **Account Settings**:
   - Click your profile picture (top right)
   - Select "Settings"

3. **GitHub Integration**:
   - Go to "Git" or "Integrations" section
   - Find "GitHub" connection
   - Click "Configure" or "Adjust GitHub App Permissions"

4. **Grant Repository Access**:
   - You'll be redirected to GitHub
   - Under "Repository access":
     - Select "Only select repositories"
     - Click "Select repositories"
     - Choose: `pilotwaffle/TORQ-Tech-News`
   - Click "Save"

### Step 2: Import Repository to Vercel

1. **New Project**:
   - Go to: https://vercel.com/new
   - You should now see `TORQ-Tech-News` in your repository list

2. **Import**:
   - Click "Import" next to `TORQ-Tech-News`

3. **Configure**:
   - **Project Name**: `torq-tech-news`
   - **Framework**: Other
   - **Root Directory**: `./`
   - **Build Settings**: Leave default
   - **Environment Variables**: None needed

4. **Deploy**:
   - Click "Deploy"
   - Wait 2-3 minutes

### Step 3: Verify Deployment

Once deployed, you'll get:
- **Production URL**: `https://torq-tech-news.vercel.app`
- **Preview URLs**: For each PR/commit

Test:
1. Visit your production URL
2. Check homepage loads
3. Verify AI/ML section
4. Test article links
5. Check admin dashboard: `/admin`

---

## 🚨 Alternative: Quick Deploy via Vercel CLI

If you want to deploy right now from terminal:

```bash
# 1. Login to Vercel (will open browser)
vercel login

# 2. Navigate to project
cd E:\sloan-review-landing

# 3. Deploy
vercel

# Follow prompts:
# - Link to existing project? No
# - Project name: torq-tech-news
# - Directory: ./
# - Override settings? No

# 4. Deploy to production
vercel --prod
```

This works with private repos because you're authenticated!

---

## ✅ Benefits of Private Repo

**Why Keep It Private:**
- ✅ Source code not publicly visible
- ✅ Protects your API keys (if any)
- ✅ Control who can see/fork your code
- ✅ Still deploys publicly to Vercel
- ✅ Professional approach

**What's Public:**
- ✅ The deployed website (vercel.app URL)
- ✅ Public can see the live site
- ❌ Public CANNOT see source code

---

## 🔧 Troubleshooting

### Issue: "Repository not found" in Vercel
**Solution**: Make sure you granted Vercel access (Step 1)

### Issue: "Permission denied"
**Solution**:
1. Go to GitHub → Settings → Applications
2. Find "Vercel"
3. Grant repository access

### Issue: Build fails
**Solution**: Check build logs in Vercel dashboard

---

## 📊 Current Status

Your repository:
- ✅ Name: `TORQ-Tech-News`
- ✅ Visibility: Private
- ✅ Local code: Up to date
- ✅ Remote: Pushed to GitHub
- ⏳ Vercel: Pending deployment

**Next**: Follow Step 1 above to grant Vercel access!

---

## 🎯 Expected Result

After completing these steps:
- 🌐 Live site: `https://torq-tech-news.vercel.app`
- 🔒 Source code: Private on GitHub
- 🤖 Auto-deploy: Every git push triggers deployment
- ⏰ Cron jobs: Running at 6AM & 11PM

---

**Ready to deploy?** Start with Step 1 above!
