# TORQ Tech News - Deployment Guide

## ✅ GitHub Repository
**Repository**: https://github.com/pilotwaffle/TOTQ-Tech-News

All code successfully pushed with 3 commits:
1. Initial commit with full AI/ML integration
2. Added requirements.txt
3. Added Vercel deployment configuration

## 📦 What's Included

### Core Files
- `app.py` - Flask application (536 lines)
- `automation_agent.py` - Content automation (407 lines)
- `index.html` - Homepage (582 lines)
- `styles.css` - MIT Sloan styling (1000+ lines)
- `script.js` - Interactive features
- `make_articles_clickable.js` - Article routing
- `populate_ai_section.js` - AI section population

### Configuration
- `requirements.txt` - Python dependencies
- `vercel.json` - Vercel deployment config
- `.gitignore` - Git exclusions
- `run.bat` - One-click Windows launcher

### Documentation
- `README.md` - Project overview
- `QUICK_START.md` - Quick reference
- `AI_ML_INTEGRATION_SUMMARY.md` - Feature documentation
- `MIT_SLOAN_DESIGN_REFERENCE.md` - Design specs
- `SYSTEM_STATUS.md` - System overview
- `DEPLOYMENT.md` - This file

### Admin
- `admin_dashboard.html` - Analytics dashboard

## 🚀 Vercel Deployment

### Option 1: Vercel CLI
```bash
npm i -g vercel
cd E:\sloan-review-landing
vercel
```

### Option 2: Vercel Dashboard
1. Go to https://vercel.com/new
2. Import from GitHub: `pilotwaffle/TOTQ-Tech-News`
3. Configure:
   - Framework Preset: Other
   - Build Command: (leave empty)
   - Output Directory: (leave empty)
4. Click "Deploy"

### Important Notes for Vercel
⚠️ **Scheduler Limitation**: Vercel is serverless, so the `schedule` library won't work as intended. You have two options:

**Option A: Use Vercel Cron Jobs**
1. Create `vercel.json` with cron configuration:
```json
{
  "crons": [
    {
      "path": "/api/update-content",
      "schedule": "0 6,23 * * *"
    }
  ]
}
```

2. Add endpoint in `app.py`:
```python
@app.route('/api/update-content')
def api_update_content():
    """Cron endpoint for Vercel"""
    import automation_agent
    agent = automation_agent.ContentAgent()
    agent.run()
    return jsonify({"status": "success"})
```

**Option B: Deploy to a Traditional Host**
- Railway.app
- Render.com
- Heroku
- DigitalOcean App Platform

These support long-running processes and the schedule library will work.

## 🔧 Local Development

### Prerequisites
- Python 3.11+
- Git

### Setup
```bash
# Clone repository
git clone https://github.com/pilotwaffle/TOTQ-Tech-News.git
cd TOTQ-Tech-News

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py

# Or use one-click launcher (Windows)
run.bat
```

### Access Points
- Main Site: http://localhost:5000
- Admin Dashboard: http://localhost:5000/admin
- Analytics API: http://localhost:5000/api/analytics

## 📊 Features

### ✅ Implemented
- [x] AI/ML content from MIT Sloan Review
- [x] Scheduled updates (6AM & 11PM)
- [x] Dedicated AI/ML section
- [x] Visitor tracking & analytics
- [x] Admin dashboard
- [x] Full article generation
- [x] Clickable article cards
- [x] MIT Sloan design theme
- [x] Responsive design
- [x] Background automation
- [x] SQLite database
- [x] Content caching

### 🔄 Scheduled Updates
**Current**: Daily at 6:00 AM and 11:00 PM
**Content**: 3 AI/ML articles + 3 general articles

### 📈 Analytics Tracked
- Unique visitors (24 hours)
- Total page views
- Top articles by views
- Recent activity feed
- Article engagement

## 🎨 Design

**Color Scheme**:
- Primary: #005b9c (MIT Sloan Blue)
- AI Section: #0097A7 (Cyan)
- Accent: #00e0ff
- Alert: #ed1b2e

**Typography**:
- Font: Inter (Google Fonts)
- Body: 1.125rem (18px)
- Headers: 800 weight

**Layout**:
- Container: 1500px max-width
- Header: 92px fixed
- Responsive breakpoints: 768px, 480px

## 🔐 Security

**Privacy Features**:
- IP hashing (SHA256)
- No personal data collection
- Session-based tracking only

**Database**:
- SQLite (gitignored)
- No sensitive data stored

## 📝 Git Workflow

```bash
# Make changes
git add .
git commit -m "feat: Your feature description"
git push

# Or use the commit template
git commit -m "$(cat <<'EOF'
feat: Your feature title

Detailed description of changes

🤖 Generated with Claude Code
https://claude.com/claude-code

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

## 🐛 Troubleshooting

### Port 5000 in use?
```bash
# Windows
netstat -ano | findstr :5000
taskkill /F /PID [process_id]

# Or just use run.bat (auto-kills old processes)
```

### Images not loading?
- Hard refresh: Ctrl + Shift + R
- Check data_cache.json for valid URLs
- Run automation_agent.py manually

### Articles not clickable?
- Hard refresh to clear cache
- Check browser console (F12) for errors
- Verify make_articles_clickable.js is loading

### Database locked?
- Close all instances of app.py
- Delete analytics.db (will be recreated)

## 📦 Dependencies

```
Flask==3.0.0          # Web framework
beautifulsoup4==4.12.2  # Web scraping
requests==2.31.0      # HTTP library
schedule==1.2.2       # Task scheduling
```

## 🌐 Environment Variables

None required! All configuration is hardcoded for simplicity.

## 📞 Support

**Repository**: https://github.com/pilotwaffle/TOTQ-Tech-News
**Issues**: https://github.com/pilotwaffle/TOTQ-Tech-News/issues

## 📄 License

MIT License - Feel free to use and modify!

---

**Last Updated**: October 16, 2025
**Status**: ✅ Production Ready
**Version**: 1.0.0

🤖 Generated with Claude Code
