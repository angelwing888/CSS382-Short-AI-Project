# Deployment Guide

Complete instructions for deploying the Marvel Rivals Balance Tracker to various platforms.

## Quick Summary of Deployment Options

| Platform | Cost | Ease | Time | Cold Start |
|----------|------|------|------|-----------|
| Heroku | Free tier available | ⭐⭐⭐⭐⭐ | 5 min | ~30s |
| Railway | Pay-per-use | ⭐⭐⭐⭐ | 5 min | ~5s |
| Render | Free tier available | ⭐⭐⭐⭐ | 10 min | ~10s |
| AWS Elastic Beanstalk | Pay-per-use | ⭐⭐⭐ | 15 min | ~5s |
| DigitalOcean | $5/month | ⭐⭐⭐ | 20 min | ~2s |
| Google Cloud | Free tier + pay | ⭐⭐⭐ | 15 min | ~10s |

---

## 1. Heroku (Easiest for Beginners)

### Pros
- ✅ Free tier available (with limitations)
- ✅ One-click deployment
- ✅ Great documentation
- ✅ Built-in PostgreSQL integration

### Cons
- ❌ Free tier has limited hours
- ❌ Apps sleep after 30 min of inactivity
- ❌ Data must be re-scraped after reboot

### Steps

1. **Create Heroku Account**
   - Go to https://www.heroku.com
   - Sign up for free

2. **Install Heroku CLI**
   ```bash
   # macOS
   brew install heroku/brew/heroku
   
   # Windows - Download installer from https://devcenter.heroku.com/articles/heroku-cli
   
   # Linux
   curl https://cli-assets.heroku.com/install.sh | sh
   ```

3. **Login**
   ```bash
   heroku login
   # Opens browser for authentication
   ```

4. **Create App** (run from project directory)
   ```bash
   heroku create your-app-name
   # Example: heroku create marvel-rivals-tracker
   ```

5. **Deploy**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push heroku main
   # OR heroku git:remote -a your-app-name && git push heroku main
   ```

6. **Populate Data**
   ```bash
   heroku run python scraper.py -a your-app-name
   ```

7. **Visit App**
   ```bash
   heroku open -a your-app-name
   ```

### Keep Data Fresh (Heroku Scheduler)

1. Add scheduler:
   ```bash
   heroku addons:create scheduler:standard -a your-app-name
   ```

2. Go to https://dashboard.heroku.com/apps/your-app-name/resources

3. Click Heroku Scheduler

4. Create a new job:
   - Command: `python scraper.py`
   - Frequency: Every day at 10:00 AM

---

## 2. Railway (Fast & Modern)

### Pros
- ✅ Generous free tier
- ✅ GitHub integration
- ✅ No cold starts
- ✅ Better performance than Heroku

### Cons
- ❌ Smaller community
- ❌ Less extensive documentation

### Steps

1. **Create Account**
   - Go to https://railway.app
   - Sign up with GitHub

2. **Connect Project**
   - Click "New Project"
   - Select "Deploy from GitHub"
   - Choose this repository

3. **Add Variables**
   - Go to Variables tab
   - Add `PYTHON_VERSION` = `3.11`

4. **Deploy**
   - Railway automatically deploys on git push
   - Watch the logs in the dashboard

5. **Populate Data**
   - Click "Command" in the top menu
   - Run: `python scraper.py`

6. **Access App**
   - Copy the public URL from the dashboard

---

## 3. Render (Best Free Tier)

### Pros
- ✅ Most generous free tier
- ✅ Auto-deploys from GitHub
- ✅ Easy to use
- ✅ No credit card required

### Cons
- ❌ Free tier sleeps after 15 min inactivity
- ❌ Slower cold starts

### Steps

1. **Create Account**
   - Go to https://render.com
   - Sign up (free)

2. **Connect GitHub**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

3. **Configure**
   - Name: `marvel-rivals-balance`
   - Environment: `Python 3`
   - Build: `pip install -r requirements.txt`
   - Start: `python scraper.py && gunicorn --bind 0.0.0.0:5000 app:app`

4. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment to complete

5. **Visit Site**
   - Copy the URL from dashboard

---

## 4. AWS Elastic Beanstalk (Professional Option)

### Pros
- ✅ Highly scalable
- ✅ Production-grade
- ✅ AWS integration
- ✅ Auto-scaling available

### Cons
- ❌ More complex setup
- ❌ Pay-per-use (but cheap for small apps)
- ❌ Steeper learning curve

### Steps

1. **Create AWS Account**
   - Go to https://aws.amazon.com
   - Create free account

2. **Install AWS CLI & EB CLI**
   ```bash
   pip install awsebcli
   aws configure
   # Enter your AWS Access Key ID and Secret Access Key
   ```

3. **Initialize Elastic Beanstalk**
   ```bash
   eb init -p python-3.11 marvel-rivals-balance
   # Select region (us-east-1 is free tier eligible)
   ```

4. **Create Environment**
   ```bash
   eb create marvel-env
   # Wait 5-10 minutes for environment to be ready
   ```

5. **Deploy**
   ```bash
   eb deploy
   ```

6. **Populate Data**
   ```bash
   eb ssh
   python scraper.py
   exit
   ```

7. **Open App**
   ```bash
   eb open
   ```

### Scheduled Scraping (AWS CloudWatch Events)

1. Go to AWS Console → CloudWatch → Events
2. Create rule with schedule: `cron(0 2 * * ? *)` (2 AM daily)
3. Add Lambda function to execute `python scraper.py` via EB SSH

---

## 5. DigitalOcean App Platform (Good Value)

### Pros
- ✅ Affordable ($5/month minimum)
- ✅ Good performance
- ✅ GitHub integration
- ✅ Straightforward pricing

### Cons
- ❌ No truly free tier
- ❌ Minimum monthly cost

### Steps

1. **Create DigitalOcean Account**
   - Go to https://digitalocean.com
   - Sign up

2. **Create App**
   - Click "Apps" → "Create App"
   - Connect GitHub repo

3. **Configure**
   - Select Python as service type
   - Build: `pip install -r requirements.txt && python scraper.py`
   - Run: `gunicorn --bind 0.0.0.0:8080 app:app`

4. **Deploy**
   - Click "Create Resources"
   - Confirm your plan (Starter: $5/month)

5. **Access**
   - Get URL from dashboard

---

## 6. Google Cloud Run (Serverless)

### Pros
- ✅ First 2 million requests free per month
- ✅ No servers to manage
- ✅ Auto-scaling
- ✅ Fast cold starts

### Cons
- ❌ May require credit card
- ❌ Complexity with persistent storage

### Steps

1. **Create Google Cloud Account**
   - Go to https://cloud.google.com
   - Enable Cloud Run and Container Registry APIs

2. **Install Google Cloud SDK**
   ```bash
   # macOS
   brew install --cask google-cloud-sdk
   
   # Other platforms: https://cloud.google.com/sdk/docs/install
   ```

3. **Authenticate**
   ```bash
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID
   ```

4. **Deploy**
   ```bash
   gcloud run deploy marvel-rivals \
     --source . \
     --platform managed \
     --region us-central1
   ```

5. **Populate Data**
   ```bash
   gcloud run jobs create scrape-balance \
     --image gcr.io/YOUR_PROJECT/marvel-rivals \
     --command="python" \
     --args="scraper.py"
   ```

---

## 7. Docker with Any Provider

If you prefer Docker, use the included `Dockerfile`:

### Deploy to Docker Hub Registry

```bash
docker build -t yourusername/marvel-rivals-balance:latest .
docker push yourusername/marvel-rivals-balance:latest
```

### Deploy with Docker Locally

```bash
docker build -t marvel-rivals .
docker run -p 5000:5000 marvel-rivals
# Visit http://localhost:5000
```

### Deploy to Container Services
- **Azure Container Instances**: https://azure.microsoft.com/services/container-instances/
- **AWS ECS**: https://aws.amazon.com/ecs/
- **DigitalOcean Kubernetes**: https://www.digitalocean.com/products/kubernetes/
- **Google Cloud Run**: (see section above)

---

## Keeping Data Fresh

### Option 1: Scheduled Scraping (Recommended)

All platforms support scheduled jobs. Set up a daily scrape:

**Command to schedule:**
```bash
python scraper.py
```

**Recommended frequency:** Daily at 2 AM UTC

### Option 2: On-Demand Updates

Manually trigger scraping:

```bash
# Heroku
heroku run python scraper.py

# AWS EB
eb ssh
python scraper.py
exit

# Railway/Render
# Use CLI or dashboard "Command" section
```

### Option 3: GitHub Actions (CI/CD)

Create `.github/workflows/scrape.yml`:

```yaml
name: Daily Scrape

on:
  schedule:
    - cron: '0 2 * * *'
  workflow_dispatch:

jobs:
  scrape:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: python scraper.py
      - run: git config user.name github-actions
      - run: git config user.email github-actions@github.com
      - run: git add balance_data.json
      - run: git commit -m "Update balance data"
      - run: git push
```

---

## Domain Setup (Optional)

To use a custom domain (e.g., `balancetracker.com`):

### Heroku
```bash
heroku domains:add balancetracker.com
# Follow DNS setup instructions
```

### Other Platforms
- Check your platform's documentation
- Usually involves updating DNS CNAME records
- Most providers offer automatic HTTPS

---

## Monitoring & Maintenance

### Check App Status
- **Heroku**: `heroku logs -t`
- **Railway**: Dashboard → Logs
- **Render**: Dashboard → Logs

### Monitor Performance
- **Response Times**: Check platform dashboard
- **Error Rates**: Review logs for errors
- **Data Freshness**: Last scrape time in logs

### Troubleshoot Issues

**App not starting:**
1. Check logs: `heroku logs` or platform equivalent
2. Verify requirements.txt syntax
3. Ensure Procfile/configuration is correct

**Data not updating:**
1. Check scheduled job logs
2. Verify scraper.py runs without errors
3. Check Marvel Rivals website is accessible

**Slow performance:**
1. Upgrade to paid tier if on free
2. Reduce worker processes if necessary
3. Check network latency to data source

---

## Cost Comparison (Annual)

- **Heroku Free**: $0 (limited)
- **Render Free**: $0 (limited)
- **Railway Free**: $5 (credit)
- **DigitalOcean**: $60 (App + Database)
- **AWS Elastic Beanstalk**: $10-50 (pay-per-use)
- **Google Cloud Run**: $0-50 (pay-per-use)

---

## Next Steps

1. Choose a platform from the options above
2. Follow the deployment steps
3. Run the scraper to populate initial data
4. Set up scheduled scraping
5. Monitor the logs
6. (Optional) Set up custom domain

**Need help?** Each platform has excellent documentation and support communities.
