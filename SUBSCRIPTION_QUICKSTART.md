# Newsletter Subscription - Quick Start

Get your newsletter subscription system running in 5 minutes.

---

## Step 1: Install Dependencies (1 min)

```bash
cd E:/TORQ-Tech-News
pip install azure-data-tables==12.4.4
```

---

## Step 2: Integrate with app.py (1 min)

Add this code to `app.py` after line 229 (after `init_data_cache()`):

```python
# Register newsletter subscription routes
try:
    from subscription_routes import register_subscription_routes
    register_subscription_routes(app)
    print("[INFO] Newsletter subscription routes registered")
except Exception as e:
    print(f"[ERROR] Error registering subscription routes: {e}")
```

---

## Step 3: Update Frontend (1 min)

Replace `script.js` with the updated version:

```bash
# Backup original
copy script.js script.js.backup

# Use updated version
copy script_updated.js script.js
```

---

## Step 4: Configure Azure (Optional, 1 min)

### Option A: With Azure Table Storage

Get your connection string from Azure Portal:
1. Go to Storage Accounts → todo69 → Access keys
2. Copy "Connection string"

Set environment variable:

**Windows (PowerShell):**
```powershell
$env:AZURE_STORAGE_CONNECTION_STRING="YOUR_CONNECTION_STRING_HERE"
```

### Option B: SQLite Only (No Config Needed)

Skip this step. System will automatically use SQLite.

---

## Step 5: Start Server (1 min)

```bash
python app.py
```

Look for this in the output:
```
[INFO] Newsletter subscription routes registered
[SUCCESS] Server starting on http://localhost:5000
```

---

## Step 6: Test It!

### In Browser:

1. Open http://localhost:5000
2. Scroll to newsletter form
3. Enter: `test@example.com`
4. Click "Subscribe"
5. See green success message!

### With curl:

```bash
curl -X POST http://localhost:5000/api/subscribe \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com"}'
```

Expected:
```json
{"success": true, "message": "Successfully subscribed!", "backend": "azure"}
```

---

## Done!

Your subscription system is live and working.

### What's Happening:

- Frontend submits email to `/api/subscribe`
- Backend validates email format
- Checks for duplicates
- Stores in Azure Table Storage (or SQLite)
- Returns success/error message
- IP addresses are hashed for privacy

---

## Verify Subscriptions

**Check Azure:**
Azure Portal → Storage Accounts → todo69 → Storage Browser → Tables → subscribers

**Check SQLite:**
```bash
sqlite3 analytics.db "SELECT email, subscribed_at, status FROM subscribers;"
```

---

## Common Issues

**"azure-data-tables not installed"**
→ Run: `pip install azure-data-tables`

**"Newsletter subscription routes registered" not showing**
→ Check app.py has the integration code from Step 2

**Frontend still shows fake success**
→ Clear browser cache and reload (Ctrl+F5)

**Backend errors in logs**
→ Check `subscribers_storage.py` and `subscription_routes.py` exist in project directory

---

## Next Steps

- Read full documentation: `SUBSCRIPTION_SETUP.md`
- Run test suite: `python test_subscription.py`
- Add Azure connection string for production
- Monitor subscriptions in Azure Portal

---

## Files Created

✓ `subscribers_storage.py` - Storage logic
✓ `subscription_routes.py` - API endpoints
✓ `script_updated.js` - Updated frontend
✓ `test_subscription.py` - Test suite
✓ `env.example` - Config template
✓ `requirements_updated.txt` - Dependencies
✓ `SUBSCRIPTION_SETUP.md` - Full documentation
✓ `SUBSCRIPTION_QUICKSTART.md` - This file

---

**Questions?** Check the full setup guide in `SUBSCRIPTION_SETUP.md`
