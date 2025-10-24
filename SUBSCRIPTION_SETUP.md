# Newsletter Subscription Setup Guide

Complete guide for setting up Azure Table Storage integration for TORQ Tech News newsletter subscriptions.

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Testing](#testing)
6. [Deployment](#deployment)
7. [Troubleshooting](#troubleshooting)

---

## Overview

This subscription system provides:

- **Dual Backend Support**: Azure Table Storage (primary) + SQLite (fallback)
- **Email Validation**: RFC 5322 compliant regex validation
- **Duplicate Detection**: Prevents duplicate subscriptions
- **Privacy**: IP address hashing (SHA-256)
- **Error Handling**: Comprehensive exception handling with logging
- **Type Safety**: Full Python type hints with mypy compatibility

---

## Architecture

```
Frontend (script_updated.js)
    |
    | POST /api/subscribe
    | {"email": "user@example.com"}
    |
Flask App (subscription_routes.py)
    |
    | validate & process
    |
SubscribersStorage (subscribers_storage.py)
    |
    |-- Try Azure Table Storage
    |       |
    |       |-- Success → Store in Azure
    |       |-- Failure → Fallback to SQLite
    |
    |-- SQLite (analytics.db)
            |
            |-- subscribers table
```

### Data Schema

**Azure Table Storage:**
```
Table Name: "subscribers"
├── PartitionKey: email_domain (e.g., "gmail.com")
├── RowKey: full_email (e.g., "user@gmail.com")
├── subscribed_at: ISO 8601 timestamp
├── source: "torqtechnews"
├── status: "active" | "unsubscribed"
└── ip_hash: SHA-256 hash (16 chars)
```

**SQLite:**
```sql
CREATE TABLE subscribers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    email_domain TEXT NOT NULL,
    subscribed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    source TEXT DEFAULT 'torqtechnews',
    status TEXT DEFAULT 'active',
    ip_hash TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

---

## Installation

### 1. Install Required Packages

```bash
pip install -r requirements_updated.txt
```

Or manually:

```bash
pip install azure-data-tables==12.4.4
```

### 2. Copy New Files

Replace/add these files in your project:

- `subscribers_storage.py` - Core storage logic
- `subscription_routes.py` - Flask API endpoints
- `script_updated.js` - Updated frontend with real API calls
- `test_subscription.py` - Test suite
- `env.example` - Environment variable template

### 3. Update app.py

Add this code after `init_data_cache()` (around line 229):

```python
# Register newsletter subscription routes
try:
    from subscription_routes import register_subscription_routes
    register_subscription_routes(app)
    print("[INFO] Newsletter subscription routes registered")
except ImportError as e:
    print(f"[WARNING] Failed to load subscription routes: {e}")
except Exception as e:
    print(f"[ERROR] Error registering subscription routes: {e}")
```

### 4. Replace script.js

```bash
# Backup original
cp script.js script.js.backup

# Use updated version
cp script_updated.js script.js
```

---

## Configuration

### Option 1: Azure Table Storage (Recommended)

1. **Get Connection String from Azure Portal:**

   ```
   1. Navigate to Azure Portal (portal.azure.com)
   2. Go to Storage Accounts → todo69
   3. Left sidebar → "Access keys"
   4. Copy "Connection string" from key1 or key2
   ```

2. **Set Environment Variable:**

   **Windows (PowerShell):**
   ```powershell
   $env:AZURE_STORAGE_CONNECTION_STRING="DefaultEndpointsProtocol=https;AccountName=todo69;AccountKey=YOUR_KEY;EndpointSuffix=core.windows.net"
   ```

   **Windows (CMD):**
   ```cmd
   set AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=todo69;AccountKey=YOUR_KEY;EndpointSuffix=core.windows.net
   ```

   **Linux/Mac:**
   ```bash
   export AZURE_STORAGE_CONNECTION_STRING="DefaultEndpointsProtocol=https;AccountName=todo69;AccountKey=YOUR_KEY;EndpointSuffix=core.windows.net"
   ```

3. **Or use .env file (with python-dotenv):**

   ```bash
   # Install dotenv
   pip install python-dotenv

   # Create .env file
   echo 'AZURE_STORAGE_CONNECTION_STRING="YOUR_CONNECTION_STRING"' > .env
   ```

   Add to app.py (at the top):
   ```python
   from dotenv import load_dotenv
   load_dotenv()
   ```

### Option 2: SQLite Only (No Configuration Needed)

If `AZURE_STORAGE_CONNECTION_STRING` is not set, the system automatically uses SQLite.

- Location: `E:/TORQ-Tech-News/analytics.db`
- Table: `subscribers`
- No additional configuration required

---

## Testing

### 1. Start the Flask Server

```bash
python app.py
```

Expected output:
```
[INFO] Newsletter subscription routes registered
[SUCCESS] Server starting on http://localhost:5000
```

### 2. Run Test Suite

```bash
pip install requests
python test_subscription.py
```

### 3. Manual Testing with curl

**Test Valid Subscription:**
```bash
curl -X POST http://localhost:5000/api/subscribe \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com"}'
```

Expected response:
```json
{
  "success": true,
  "message": "Successfully subscribed!",
  "backend": "azure"
}
```

**Test Duplicate Email:**
```bash
curl -X POST http://localhost:5000/api/subscribe \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com"}'
```

Expected response:
```json
{
  "success": false,
  "error": "Email already subscribed"
}
```

**Test Invalid Email:**
```bash
curl -X POST http://localhost:5000/api/subscribe \
  -H "Content-Type: application/json" \
  -d '{"email": "invalid-email"}'
```

Expected response:
```json
{
  "success": false,
  "error": "Invalid email format"
}
```

**Get Subscriber Count:**
```bash
curl http://localhost:5000/api/subscribers/count
```

Expected response:
```json
{
  "success": true,
  "count": 1,
  "backend": "azure"
}
```

### 4. Test in Browser

1. Navigate to http://localhost:5000
2. Scroll to "Subscribe" section
3. Enter email address
4. Click "Subscribe" button
5. Check for success message (green notification)

---

## Deployment

### Vercel Deployment

1. **Add Environment Variable:**

   ```bash
   vercel env add AZURE_STORAGE_CONNECTION_STRING
   ```

   Or via Vercel Dashboard:
   - Project Settings → Environment Variables
   - Add `AZURE_STORAGE_CONNECTION_STRING`
   - Paste connection string
   - Select all environments (Production, Preview, Development)

2. **Deploy:**

   ```bash
   vercel --prod
   ```

### Railway Deployment

1. **Add Environment Variable:**

   - Railway Dashboard → Your Project
   - Variables tab
   - Add `AZURE_STORAGE_CONNECTION_STRING`
   - Paste connection string

2. **Redeploy:**

   ```bash
   git push
   ```

### Heroku Deployment

```bash
heroku config:set AZURE_STORAGE_CONNECTION_STRING="YOUR_CONNECTION_STRING"
git push heroku main
```

---

## Troubleshooting

### Issue: "azure-data-tables package not installed"

**Solution:**
```bash
pip install azure-data-tables==12.4.4
```

### Issue: "Failed to initialize Azure Table Storage"

**Causes:**
1. Invalid connection string
2. Incorrect storage account name
3. Network issues

**Solution:**
1. Verify connection string format
2. Test connection:
   ```python
   from azure.data.tables import TableServiceClient
   conn_str = "YOUR_CONNECTION_STRING"
   service = TableServiceClient.from_connection_string(conn_str)
   tables = list(service.list_tables())
   print(f"Connected! Tables: {[t.name for t in tables]}")
   ```

### Issue: "Email already subscribed" but shouldn't be

**Solution:**
Check both Azure and SQLite:

**Azure:**
```python
from azure.data.tables import TableServiceClient
import os
conn_str = os.environ['AZURE_STORAGE_CONNECTION_STRING']
service = TableServiceClient.from_connection_string(conn_str)
table = service.get_table_client("subscribers")
for entity in table.list_entities():
    print(f"{entity['RowKey']} - {entity['status']}")
```

**SQLite:**
```bash
sqlite3 analytics.db "SELECT * FROM subscribers;"
```

### Issue: Frontend shows "Failed to subscribe"

**Diagnosis:**
1. Check browser console (F12) for errors
2. Check Flask logs for exceptions
3. Verify API endpoint is accessible:
   ```bash
   curl -X POST http://localhost:5000/api/subscribe \
     -H "Content-Type: application/json" \
     -d '{"email": "test@example.com"}'
   ```

### Issue: Slow subscription response

**Causes:**
1. Azure Table Storage latency
2. Network issues

**Solution:**
- Azure typically responds in <200ms
- SQLite fallback responds in <50ms
- Check `result.storage_backend` in response to see which was used
- Consider caching or async processing for high volume

---

## API Reference

### POST /api/subscribe

Subscribe an email address to the newsletter.

**Request:**
```json
{
  "email": "user@example.com"
}
```

**Response (Success):**
```json
{
  "success": true,
  "message": "Successfully subscribed!",
  "backend": "azure"
}
```

**Response (Validation Error):**
```json
{
  "success": false,
  "error": "Invalid email format"
}
```

**Response (Duplicate):**
```json
{
  "success": false,
  "error": "Email already subscribed"
}
```

**Status Codes:**
- `200`: Success
- `400`: Validation error (invalid email)
- `409`: Duplicate subscription
- `500`: Server error

### GET /api/subscribers/count

Get total active subscriber count.

**Response:**
```json
{
  "success": true,
  "count": 1234,
  "backend": "azure"
}
```

---

## Security Considerations

1. **IP Hashing**: All IP addresses are SHA-256 hashed before storage
2. **Email Storage**: Emails stored in lowercase for consistency
3. **No Secrets in Code**: Connection strings via environment variables only
4. **Input Validation**: RFC 5322 compliant email regex
5. **HTTPS Required**: Always use HTTPS in production
6. **Rate Limiting**: Consider adding rate limiting for production:
   ```python
   from flask_limiter import Limiter
   limiter = Limiter(app, default_limits=["5 per minute"])

   @limiter.limit("3 per minute")
   @app.route('/api/subscribe', methods=['POST'])
   def subscribe():
       ...
   ```

---

## Monitoring

### Check Azure Table Storage

**Azure Portal:**
1. Storage Account → todo69
2. Storage Browser → Tables → subscribers
3. View all entities

**Python:**
```python
from azure.data.tables import TableServiceClient
import os

conn_str = os.environ['AZURE_STORAGE_CONNECTION_STRING']
service = TableServiceClient.from_connection_string(conn_str)
table = service.get_table_client("subscribers")

# Count active subscribers
active = sum(1 for e in table.list_entities() if e['status'] == 'active')
print(f"Active subscribers: {active}")
```

### Check SQLite

```bash
sqlite3 analytics.db << EOF
SELECT
    COUNT(*) as total,
    SUM(CASE WHEN status = 'active' THEN 1 ELSE 0 END) as active
FROM subscribers;
EOF
```

---

## Next Steps

1. **Add Email Confirmation**: Send confirmation emails using SendGrid/Mailgun
2. **Unsubscribe Feature**: Add /api/unsubscribe endpoint
3. **Admin Dashboard**: View subscribers in admin panel
4. **Export Feature**: Export subscriber list to CSV
5. **Analytics**: Track subscription sources and conversion rates
6. **A/B Testing**: Test different subscription form designs
7. **GDPR Compliance**: Add privacy policy links and data export

---

## Support

For issues or questions:

1. Check logs: Flask console output
2. Review test results: `python test_subscription.py`
3. Verify configuration: Environment variables set correctly
4. Check Azure Portal: Storage account accessible

---

## License

Part of TORQ Tech News project. All rights reserved.
