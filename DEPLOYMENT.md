# Deployment Guide for Terminal Archives

## Why This App Cannot Be Deployed to GitHub Pages

GitHub Pages is designed for **static websites only** (HTML, CSS, JavaScript). It does not support:
- Backend servers (Python/Flask)
- Server-side processing
- File uploads
- Dynamic routing
- Database operations

**Terminal Archives** is a Flask application that requires:
- Python runtime environment
- Server-side file processing
- Dynamic route handling
- PDF manipulation on the server

Therefore, you need a platform that supports Python web applications.

## Recommended Deployment Platforms

### 1. Heroku (Easiest - Free Tier Available)

#### Prerequisites
- Heroku account
- Heroku CLI installed

#### Steps
```bash
# Login to Heroku
heroku login

# Create a new Heroku app
heroku create your-app-name

# Add buildpack
heroku buildpacks:set heroku/python

# Set environment variables
heroku config:set SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
heroku config:set FLASK_ENV=production

# Create Procfile
echo "web: gunicorn app:app" > Procfile

# Create runtime.txt
echo "python-3.11.0" > runtime.txt

# Deploy
git add .
git commit -m "Prepare for Heroku deployment"
git push heroku main

# Open your app
heroku open
```

### 2. PythonAnywhere (Free Tier Available)

#### Steps
1. Sign up at [pythonanywhere.com](https://www.pythonanywhere.com)
2. Upload your code or clone from GitHub
3. Create a new web app (Flask)
4. Set up virtualenv and install requirements
5. Configure WSGI file
6. Set environment variables in web app settings
7. Reload the web app

#### Example WSGI Configuration
```python
import sys
import os

# Add your project directory to the sys.path
project_home = '/home/yourusername/termial-archieve-before-SQLite-imp'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment variables
os.environ['SECRET_KEY'] = 'your-secret-key'
os.environ['FLASK_ENV'] = 'production'

# Import Flask app
from app import app as application
```

### 3. Railway (Modern Platform)

#### Steps
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Set environment variables
railway variables set SECRET_KEY=your-secret-key
railway variables set FLASK_ENV=production

# Deploy
railway up
```

### 4. Render (Free Tier Available)

#### Steps
1. Sign up at [render.com](https://render.com)
2. Create a new Web Service
3. Connect your GitHub repository
4. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
5. Add environment variables
6. Deploy

### 5. DigitalOcean App Platform

#### Steps
1. Sign up at DigitalOcean
2. Create a new App
3. Connect GitHub repository
4. Configure environment variables
5. Deploy

### 6. AWS EC2 (Advanced)

#### Prerequisites
- AWS account
- Basic Linux knowledge

#### Steps
1. Launch EC2 instance (Ubuntu recommended)
2. SSH into instance
3. Install Python and dependencies
4. Clone repository
5. Install Nginx and configure reverse proxy
6. Set up Gunicorn as service
7. Configure SSL with Let's Encrypt

## Post-Deployment Steps

### 1. Configure Environment Variables
Set these on your hosting platform:
```
SECRET_KEY=<your-generated-secret-key>
FLASK_ENV=production
```

### 2. Set Up Database (Future Enhancement)
For production, consider migrating to SQLite or PostgreSQL:
```bash
# For SQLite (simple)
pip install flask-sqlalchemy

# For PostgreSQL (recommended for production)
pip install psycopg2-binary flask-sqlalchemy
```

### 3. Configure File Storage
For production with multiple servers, consider:
- AWS S3
- Google Cloud Storage
- DigitalOcean Spaces
- Cloudinary

### 4. Set Up Monitoring
- Application monitoring: Sentry, New Relic
- Uptime monitoring: UptimeRobot, Pingdom
- Log management: Papertrail, Loggly

### 5. Enable HTTPS
Most platforms provide free SSL:
- Heroku: Automatic with paid dynos
- PythonAnywhere: Available on paid plans
- Railway/Render: Automatic and free
- Custom server: Use Let's Encrypt

## Platform-Specific Configuration Files

### Procfile (Heroku, Railway)
```
web: gunicorn app:app --bind 0.0.0.0:$PORT
```

### runtime.txt (Heroku)
```
python-3.11.0
```

### render.yaml (Render)
```yaml
services:
  - type: web
    name: terminal-archives
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app
    envVars:
      - key: FLASK_ENV
        value: production
      - key: SECRET_KEY
        generateValue: true
```

### .dockerignore (Docker deployment)
```
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env
venv
.env
.git
.gitignore
uploads/
```

### Dockerfile (Docker deployment)
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p uploads

ENV FLASK_ENV=production
ENV SECRET_KEY=change-this-in-production

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

## Troubleshooting Common Deployment Issues

### Issue: App crashes on startup
**Solution**: Check logs for missing dependencies or environment variables

### Issue: Static files not loading
**Solution**: Ensure static folder is in correct location, check file paths

### Issue: File uploads failing
**Solution**: Check write permissions on uploads directory

### Issue: Memory errors
**Solution**: Reduce number of workers or upgrade to larger instance

### Issue: Slow performance
**Solution**: 
- Enable gzip compression
- Use CDN for static files
- Optimize PDF processing
- Add caching

## Cost Estimates

### Free Options
- **Heroku**: Free tier (sleeps after 30 min inactivity)
- **PythonAnywhere**: Free tier (limited CPU)
- **Render**: Free tier (spins down after inactivity)
- **Railway**: $5 free credit monthly

### Paid Options (Recommended for Production)
- **Heroku Hobby**: $7/month
- **PythonAnywhere Hacker**: $5/month
- **Render Starter**: $7/month
- **Railway**: ~$5-10/month
- **DigitalOcean Droplet**: $6/month (1GB RAM)

## Performance Optimization

### For Production Deployment
1. Use Gunicorn with multiple workers
2. Enable gzip compression
3. Set up caching headers
4. Use CDN for static files
5. Optimize images and assets
6. Monitor and scale as needed

## Scaling Considerations

### Vertical Scaling (Easier)
- Increase server resources (RAM, CPU)
- Suitable for most small to medium applications

### Horizontal Scaling (Advanced)
- Multiple server instances
- Load balancer
- Shared file storage (S3, etc.)
- Distributed caching (Redis)

## Support and Resources

- Flask Documentation: https://flask.palletsprojects.com/
- Gunicorn Documentation: https://gunicorn.org/
- Platform-specific documentation:
  - Heroku: https://devcenter.heroku.com/
  - PythonAnywhere: https://help.pythonanywhere.com/
  - Railway: https://docs.railway.app/
  - Render: https://render.com/docs

## Next Steps After Deployment

1. Test all functionality in production environment
2. Set up monitoring and alerts
3. Configure automated backups
4. Document your deployment process
5. Create runbook for common issues
6. Plan for scaling as usage grows
7. Consider adding authentication
8. Implement analytics
9. Regular security updates
10. User feedback collection
