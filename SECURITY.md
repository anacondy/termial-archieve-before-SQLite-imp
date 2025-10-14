# Security Best Practices for Terminal Archives

## Environment Variables Setup

### Generate a Secure Secret Key
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Set Environment Variables

#### On Windows (PowerShell)
```powershell
$env:SECRET_KEY="your-generated-key-here"
$env:FLASK_ENV="production"
```

#### On Windows (Command Prompt)
```cmd
set SECRET_KEY=your-generated-key-here
set FLASK_ENV=production
```

#### On macOS/Linux
```bash
export SECRET_KEY="your-generated-key-here"
export FLASK_ENV="production"
```

#### Using .env file (recommended)
Create a `.env` file in the project root:
```
SECRET_KEY=your-generated-key-here
FLASK_ENV=production
```

Then use python-dotenv to load it:
```bash
pip install python-dotenv
```

Add to your app.py:
```python
from dotenv import load_dotenv
load_dotenv()
```

## Production Deployment Checklist

### Security
- [ ] Set `FLASK_ENV=production`
- [ ] Set a strong `SECRET_KEY` (32+ characters, random)
- [ ] Never commit `.env` files to version control
- [ ] Use HTTPS/SSL certificates
- [ ] Configure firewall rules
- [ ] Set up fail2ban or similar intrusion prevention
- [ ] Regular security audits with `bandit` and `safety`

### Performance
- [ ] Use production WSGI server (Gunicorn recommended)
- [ ] Enable gzip compression
- [ ] Configure caching headers
- [ ] Set up CDN for static files
- [ ] Monitor resource usage

### Reliability
- [ ] Set up automated backups for uploads directory
- [ ] Configure logging to file
- [ ] Set up error monitoring (e.g., Sentry)
- [ ] Create health check endpoint
- [ ] Document recovery procedures

### Maintenance
- [ ] Keep dependencies updated
- [ ] Regular vulnerability scanning
- [ ] Monitor disk space (uploads folder)
- [ ] Log rotation setup
- [ ] Backup verification

## Running with Gunicorn (Production)

```bash
pip install gunicorn

# Basic usage
gunicorn -w 4 -b 0.0.0.0:8000 app:app

# With recommended settings
gunicorn -w 4 -b 0.0.0.0:8000 --access-logfile logs/access.log --error-logfile logs/error.log --log-level info app:app
```

## Nginx Configuration Example

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /path/to/your/app/static;
        expires 30d;
    }

    location /uploads {
        alias /path/to/your/app/uploads;
        expires 7d;
    }
}
```

## Security Scanning

### Run Bandit (Python security linter)
```bash
pip install bandit
bandit -r . -x ./venv
```

### Check for vulnerable dependencies
```bash
pip install safety
safety check
```

### Check for outdated dependencies
```bash
pip list --outdated
```

## Rate Limiting Configuration

Current limits (in app.py):
- Default: 200 requests per day, 50 per hour
- Upload endpoint: 10 uploads per hour

To adjust, modify the `@limiter.limit()` decorators in app.py.

## File Upload Security

Current restrictions:
- Maximum file size: 50 MB
- Allowed file types: PDF only
- Filename sanitization: Automatic
- Path traversal prevention: Enabled

## Common Security Issues to Avoid

1. **Never commit secrets**: Use .env files and .gitignore
2. **Don't run with debug=True in production**: Check FLASK_ENV
3. **Validate all inputs**: Already implemented in sanitize()
4. **Limit file sizes**: Already configured (50 MB)
5. **Use HTTPS**: Configure at server/reverse proxy level
6. **Regular updates**: Keep Flask and dependencies updated
7. **Monitor logs**: Set up log monitoring for suspicious activity
8. **Backup regularly**: Automate backup of uploads directory

## Monitoring Recommendations

- Set up application performance monitoring (APM)
- Configure alerts for:
  - High error rates
  - Unusual traffic patterns
  - Disk space warnings
  - Memory usage spikes
- Review logs regularly for:
  - Failed login attempts (if auth added)
  - Unusual upload patterns
  - Error patterns

## Contact Security Issues

If you discover a security vulnerability, please email the maintainer directly rather than opening a public issue.
