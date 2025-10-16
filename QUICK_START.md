# MIT Sloan Review - Quick Start Guide

## 🚀 One-Click Launch

**Double-click**: `run.bat`

That's it! The system will:
1. Clean up old processes
2. Start the web server
3. Open your browser automatically

## 📍 Access Points

- **Main Site**: http://localhost:5000
- **Admin Dashboard**: http://localhost:5000/admin
- **Analytics API**: http://localhost:5000/api/analytics

## 🎯 Key Features

### ✅ Working Now
- Clickable articles with full generated content
- Real-time visitor tracking
- Admin dashboard with analytics
- Automated content updates (hourly)
- MIT Sloan blue design theme
- Working images from Unsplash

### 📊 What's Tracked
- Visitors (last 24 hours)
- Total page views
- Top articles by views
- Recent activity feed

## 🔧 Manual Commands

### Start Server
```bash
cd E:\sloan-review-landing
"E:\Python\Python311\python.exe" app.py
```

### Run Content Update
```bash
cd E:\sloan-review-landing
"E:\Python\Python311\python.exe" automation_agent.py
```

### Stop Server
Press `Ctrl+C` in the server window, or close the window

## 📁 Essential Files

| File | Purpose |
|------|---------|
| `run.bat` | One-click launcher (USE THIS) |
| `app.py` | Main Flask application |
| `automation_agent.py` | Content updater |
| `index.html` | Homepage template |
| `styles.css` | MIT Sloan styling |
| `analytics.db` | Visitor database |
| `data_cache.json` | Article cache |

## 🎨 Design Colors

- **Primary**: #005b9c (MIT Sloan Blue)
- **Accent**: #00e0ff (Cyan)
- **Alert**: #ed1b2e (Red)

## 🤖 Automation

Content updates **automatically at 6:00 AM and 11:00 PM daily** while server runs.

Features:
- 3 AI/ML articles from MIT Sloan's Data & AI topic
- 3 general business articles
- Dedicated AI/ML section on homepage
- Auto-refresh on server startup

Manual update: Run `automation_agent.py`

## ⚠️ Troubleshooting

**Port 5000 in use?**
```bash
netstat -ano | findstr :5000
taskkill //F //PID [process_id]
```

**Images not loading?**
- Hard refresh: `Ctrl + Shift + R`
- Check `data_cache.json` for image URLs

**Articles not clickable?**
- Hard refresh to get updated JavaScript
- Check browser console (F12) for errors

## 📖 Documentation

- `SYSTEM_STATUS.md` - Complete system overview
- `MIT_SLOAN_DESIGN_REFERENCE.md` - Design specifications
- `README.md` - Full documentation

---

**Quick Start**: Double-click `run.bat` → Everything works! 🎉
