# YCBN Production Deployment Guide (Ubuntu + Nginx + Gunicorn + Let’s Encrypt)

This guide turns your Django app into a production service with HTTPS.

Prerequisites
- Ubuntu server with sudo access
- DNS A/AAAA records for ycbn.org and www.ycbn.org pointing to your server
- Python 3.10+ recommended

1) Create a virtualenv and install production deps
- python3 -m venv /home/oluwa/Documents/ycbncharity/.venv
- source /home/oluwa/Documents/ycbncharity/.venv/bin/activate
- pip install --upgrade pip
- pip install -r deploy/requirements.production.txt
- python -m pip check

2) Collect static files (optional now; recommended before enabling Nginx static)
- python manage.py collectstatic --noinput --settings=ycbn_charity.settings_production
  - STATIC_ROOT is configured at staticfiles/
  - Optionally rsync staticfiles/ to /var/www/static and enable Nginx static blocks

3) Configure systemd (Gunicorn service)
- sudo cp deploy/systemd/ycbn.service /etc/systemd/system/ycbn.service
- sudo systemctl daemon-reload
- sudo systemctl enable ycbn
- sudo systemctl start ycbn
- sudo systemctl status ycbn

Notes:
- Edit /etc/systemd/system/ycbn.service to adjust paths and add secrets via Environment or an EnvironmentFile.
- Set DJANGO_SECRET_KEY and DATABASE_URL securely via systemd drop-in: sudo systemctl edit ycbn

4) Install and configure Nginx
- sudo apt update && sudo apt install -y nginx
- sudo cp deploy/nginx/ycbn.org.conf /etc/nginx/sites-available/ycbn.org
- sudo ln -s /etc/nginx/sites-available/ycbn.org /etc/nginx/sites-enabled/ycbn.org
- sudo nginx -t && sudo systemctl reload nginx

5) Obtain HTTPS certificate (Let’s Encrypt)
- sudo snap install core; sudo snap refresh core
- sudo snap install --classic certbot
- sudo ln -s /snap/bin/certbot /usr/bin/certbot
- sudo certbot --nginx -d ycbn.org -d www.ycbn.org --redirect -m you@example.com -n --agree-tos

This injects SSL paths into the Nginx config and sets automated renewals (/etc/cron.d or systemd timers).

6) Verify
- curl -I http://ycbn.org      # expect 301 to https
- curl -I https://ycbn.org     # expect 200 and Strict-Transport-Security
- In browser: https://ycbn.org

7) Environment variables (production)
Set via systemd Environment or /etc/default/ycbn (EnvironmentFile) and reference in the unit:
- DJANGO_SETTINGS_MODULE=ycbn_charity.settings_production
- DJANGO_SECRET_KEY=your_production_secret
- DJANGO_ALLOWED_HOSTS=ycbn.org,www.ycbn.org
- SITE_BASE_URL=https://ycbn.org
- DATABASE_URL=postgres://user:pass@host:5432/dbname (optional)
- USE_WHITENOISE=true (optional; if not serving static via Nginx)

8) Logs and troubleshooting
- journalctl -u ycbn -f
- sudo nginx -t && sudo systemctl reload nginx
- Check app logs from gunicorn (stdout/stderr)

9) Performance and security
- Adjust Gunicorn workers based on CPU cores in gunicorn.conf.py
- If behind a load balancer, ensure it passes X-Forwarded-Proto=https
- With DEBUG=False, Django security headers and HTTPS redirects are active

10) Zero-downtime deploys
- sudo systemctl restart ycbn  # simple restart
- For advanced: use gunicorn --graceful-timeout and USR2 signals (optional)
