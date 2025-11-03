# CI/CD Setup Guide

## Overview

This project uses GitHub Actions for continuous integration and deployment to Railway.app.

## Prerequisites

1. GitHub repository with the project
2. Railway.app account
3. Railway project created and linked to the repository

## Setup Instructions

### 1. Railway Setup

1. Go to [Railway.app](https://railway.app)
2. Create a new project or use existing one
3. Connect your GitHub repository
4. Railway will automatically detect the Python app

#### Environment Variables on Railway

Set these in Railway Dashboard → Your Project → Variables:

```env
FLASK_ENV=production
PYTHONUNBUFFERED=1
AUTO_UPDATE_INTERVAL=5
```

**Note**: Railway automatically sets `PORT` - do not override it.

### 2. GitHub Secrets Setup

Add these secrets in your GitHub repository:

1. Go to: `Settings` → `Secrets and variables` → `Actions`
2. Click `New repository secret`
3. Add the following secrets:

#### Required Secrets

**RAILWAY_TOKEN**
- Description: Railway API token for deployments
- How to get:
  1. Go to Railway Dashboard
  2. Click your profile → Account Settings
  3. Go to "Tokens" section
  4. Click "Create Token"
  5. Copy the token and paste it as secret value

**RAILWAY_SERVICE_ID** (Optional)
- Description: Specific service ID to deploy to
- How to get:
  1. Go to your Railway project
  2. Click on your service
  3. Go to Settings
  4. Copy the Service ID from the URL or settings page

### 3. GitHub Actions Workflows

This project has two workflows:

#### `deploy.yml` - Main CI/CD Pipeline

**Triggers**:
- Push to `main` branch
- Pull requests to `main`
- Manual trigger via GitHub Actions UI

**Jobs**:
1. **Test and Lint**
   - Lints code with flake8
   - Scans for potential secrets
   - Runs basic import tests
   - Validates database initialization

2. **Deploy** (only on main branch pushes)
   - Deploys to Railway automatically
   - Only runs if tests pass

#### `update-articles.yml` - Content Update

**Triggers**:
- Scheduled: Daily at 6 AM UTC
- Manual trigger

**Purpose**:
- Automatically updates article content from sources
- Commits changes back to repository

## Deployment Process

### Automatic Deployment

1. Make changes to your code
2. Commit and push to a feature branch
3. Create a Pull Request to `main`
4. CI tests will run automatically
5. Once PR is merged to `main`, deployment happens automatically

### Manual Deployment

1. Go to GitHub → Actions tab
2. Select "Test and Deploy to Railway" workflow
3. Click "Run workflow"
4. Select `main` branch
5. Click "Run workflow"

## CI/CD Pipeline Details

### Test Stage

```yaml
- Install dependencies from requirements.txt
- Run flake8 linter
  - Stop on syntax errors (E9, F63, F7, F82)
  - Warn on complexity/style issues
- Scan for exposed secrets
- Test Python imports
- Validate database initialization
```

### Deploy Stage

```yaml
- Install Railway CLI
- Authenticate with RAILWAY_TOKEN
- Deploy to Railway service
- Report deployment status
```

## Monitoring Deployments

### Railway Dashboard

1. Go to [Railway Dashboard](https://railway.app/dashboard)
2. Select your project
3. View deployment logs in real-time
4. Check service health and metrics

### GitHub Actions

1. Go to repository → Actions tab
2. See all workflow runs and their status
3. Click on any run to see detailed logs
4. Download logs for debugging

## Troubleshooting

### Deployment Fails

1. **Check GitHub Actions logs**
   - Look for error messages in test or deploy stages

2. **Check Railway logs**
   - Go to Railway Dashboard → Your Service → Deployments
   - View build and runtime logs

3. **Common issues**:
   - Missing environment variables
   - Invalid Railway token
   - Dependency installation failures
   - Port binding issues (Railway sets PORT automatically)

### Tests Fail

1. **Linting errors**:
   - Run `flake8 .` locally to see issues
   - Fix code style issues

2. **Import errors**:
   - Check that all dependencies are in `requirements.txt`
   - Verify Python version compatibility (3.11+)

3. **Database errors**:
   - Ensure SQLite is available
   - Check file permissions

### Railway Token Expired

1. Generate new token in Railway Dashboard
2. Update `RAILWAY_TOKEN` secret in GitHub
3. Re-run failed deployment

## Best Practices

### Before Pushing

```bash
# Run linter locally
flake8 .

# Run tests
python -m pytest tests/

# Check for secrets
grep -r "sk-" . --exclude-dir=.git
```

### Feature Development

1. Create feature branch from `main`
2. Make changes and test locally
3. Push branch and create PR
4. Wait for CI tests to pass
5. Merge to `main` after approval
6. Automatic deployment will trigger

### Rollback

If a deployment has issues:

1. Go to Railway Dashboard
2. Select the service
3. Click "Deployments"
4. Find the last working deployment
5. Click "Redeploy"

Or revert the commit on GitHub and push.

## Security Notes

- Never commit secrets to the repository
- Use GitHub Secrets for sensitive values
- Railway environment variables are encrypted
- Rotate tokens periodically
- Review CI logs for exposed credentials

## Monitoring & Alerts

### Health Checks

The app provides health check endpoints:
- `/health` - Overall system health
- `/api/health` - Detailed health status

Railway can monitor these endpoints automatically.

### Logs

View application logs:
```bash
# Via Railway CLI
railway logs

# Via Railway Dashboard
Dashboard → Service → View Logs
```

## Support

- Railway Docs: https://docs.railway.app
- GitHub Actions Docs: https://docs.github.com/actions
- Project Issues: https://github.com/pilotwaffle/TORQ-Tech-News/issues
