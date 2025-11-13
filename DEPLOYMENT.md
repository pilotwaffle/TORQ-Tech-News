# TORQ Tech News - Production Deployment Guide

## ✅ Production-Ready Configuration

This application is configured for production deployment on Railway with the following optimizations:

### 🚀 Production WSGI Server

**Gunicorn** with gevent worker class for high-performance async handling:

```bash
gunicorn --bind 0.0.0.0:$PORT \
  --workers 4 \
  --threads 2 \
  --worker-class gevent \
  --timeout 120 \
  --access-logfile - \
  --error-logfile - \
  app:app
```

**Configuration Details:**
- **Workers:** 4 (optimal for Railway's standard instance)
- **Threads:** 2 per worker
- **Worker Class:** gevent (async I/O for content scraping)
- **Timeout:** 120 seconds (handles long-running content extraction)
- **Logging:** stdout/stderr for Railway log integration

---

## 📦 Deployment Files

### `requirements.txt`
Production dependencies including:
- Flask 3.0.0
- Gunicorn 21.2.0 (production WSGI server)
- gevent 24.2.1 (async worker)
- beautifulsoup4, requests (content scraping)
- newspaper3k (article extraction)

### `railway.toml`
Railway-specific configuration:
- Builder: Dockerfile
- Start Command: Gunicorn with production settings

### `Procfile`
Alternative process definition (Railway uses railway.toml by default):
```
web: gunicorn ... app:app
```

### `Dockerfile`
Optimized Docker build:
- Base: python:3.11-slim
- Dynamic PORT binding (Railway assigns automatically)
- Environment variables for Flask production mode

---

## 🔧 Railway Environment Variables

Set these in your Railway dashboard:

**Required:**
- `PORT` - Automatically set by Railway (do not override)
- `FLASK_ENV=production`
- `PYTHONUNBUFFERED=1`

**Optional:**
- `AUTO_UPDATE_INTERVAL` - Content update frequency (default: 5 hours)
- API keys for premium content sources

---

## 📊 Features

### Endpoints
- `/` - Main application
- `/admin` - Admin dashboard
- `/api/analytics` - Analytics API
- `/api/analytics/advanced` - Advanced analytics

### Content Sources
- TechCrunch
- MIT Technology Review
- Hacker News
- MIT Sloan Review

### Auto-Update
- Background thread runs every 5 hours
- Scrapes and extracts full article content
- Caches results in `data_cache.json`
- Advanced analytics in SQLite database

---

## ⚠️ Production Considerations

### Database
Currently using **SQLite** (`analytics.db`):
- ✅ Simple, no external dependencies
- ⚠️ Ephemeral in Docker (resets on redeploy)
- 💡 **Recommendation:** Upgrade to Railway PostgreSQL for persistence

### Storage
- `data_cache.json` - Content cache (ephemeral)
- **Solution:** Mount Railway volume or use external storage (S3, Railway Volume)

### Scaling
- Current: 4 workers, handles moderate traffic
- For high traffic: Increase workers or horizontal scaling

---

## 🚀 Deployment Workflow

1. **Push to GitHub:**
   ```bash
   git push origin main
   ```

2. **Railway Auto-Deploy:**
   - Detects changes
   - Builds Docker image
   - Deploys with Gunicorn
   - Assigns public URL

3. **Monitor Logs:**
   ```bash
   railway logs
   ```

4. **Check Health:**
   - Visit deployment URL
   - Check `/api/analytics` endpoint
   - Verify content aggregation running

---

## 🐛 Troubleshooting

### Common Issues

**Port Binding:**
- Ensure app.py uses: `port = int(os.environ.get('PORT', 5000))`
- Railway sets PORT dynamically

**Worker Timeout:**
- Content scraping can take time
- Timeout set to 120s to accommodate

**Memory Limits:**
- 4 workers + gevent = ~512MB usage
- Railway standard instances have sufficient memory

**Database Resets:**
- SQLite resets on redeploy
- Upgrade to PostgreSQL for persistence

---

## 📈 Performance Metrics

**Expected Performance:**
- Concurrent Requests: 50-100 (with gevent)
- Response Time: <500ms (cached content)
- Content Update: Every 5 hours (background)
- Memory Usage: ~512MB
- CPU Usage: Low (async I/O)

---

## 🔐 Security Best Practices

✅ Production WSGI server (Gunicorn)
✅ Environment variables for sensitive data
✅ No hardcoded credentials
✅ Debug mode disabled in production
✅ HTTPS via Railway (automatic)

---

## 📝 Maintenance

### Update Dependencies
```bash
pip list --outdated
pip install --upgrade [package]
```

### Database Migrations
Currently manual - consider adding Flask-Migrate for schema changes

### Log Monitoring
Use Railway dashboard or CLI:
```bash
railway logs --tail 100
```

---

## 🎯 Future Enhancements

- [ ] PostgreSQL migration for data persistence
- [ ] Redis caching for improved performance
- [ ] Celery for distributed background tasks
- [ ] API rate limiting
- [ ] Authentication for admin endpoints
- [ ] Prometheus metrics export
- [ ] Health check endpoint

---

**Deployed with ❤️ using Railway**

---

## 🌐 Railway Private Networking Optimization

### IPv6 Dual-Stack Binding

The application is configured with Railway's recommended IPv6 binding:

```bash
gunicorn --bind [::]:$PORT
```

**Benefits:**
- ✅ **Dual-stack support:** Accepts both IPv4 (public) and IPv6 (private network)
- ✅ **Private networking ready:** Compatible with Railway's internal service mesh
- ✅ **Future-proof:** Prepared for microservices architecture
- ✅ **Railway best practice:** Aligns with official documentation

### Private Networking Status

**Current Architecture:** Single-service deployment
- Public domain: `torqtechnews.com` and `www.torqtechnews.com`
- Railway internal domain: `[service-name].railway.internal` (available but not used)

**Private networking is enabled by default** on all Railway projects but currently not utilized since this is a single-service deployment.

### Future Microservices Architecture

When scaling to multiple services, private networking enables secure service-to-service communication:

```
Frontend (Public) → API (Private) → Database (Private)
  torqtechnews.com     api.railway.internal     postgres.railway.internal
```

**Configuration for future services:**
```bash
# Frontend environment variables
BACKEND_URL=http://${{api.RAILWAY_PRIVATE_DOMAIN}}:${{api.PORT}}

# API environment variables  
DATABASE_URL=${{postgres.DATABASE_URL}}
```

### DNS Configuration

Custom domain configured via Namecheap:
- **Root domain:** CNAME @ → `web-production-e23a.up.railway.app`
- **WWW subdomain:** CNAME www → `web-production-e23a.up.railway.app`
- **TTL:** 30 minutes (automatic for root, 30min for www)

---

**Last Updated:** 2025-10-22
**IPv6 Optimization:** Implemented
**Private Networking:** Ready for future use
