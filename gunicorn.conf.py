# Gunicorn configuration for YCBN
# Start with: gunicorn -c gunicorn.conf.py ycbn_charity.wsgi:application

import multiprocessing

wsgi_app = "ycbn_charity.wsgi:application"
# Bind to loopback; Nginx will reverse proxy to this
bind = "127.0.0.1:8000"
# Workers: 2-4 x CPU cores is typical; start conservative
workers = max(2, multiprocessing.cpu_count())
threads = 2
worker_class = "gthread"
# Keep-alive and timeouts
keepalive = 65
timeout = 60
# Restart workers periodically to mitigate memory leaks
max_requests = 1000
max_requests_jitter = 100
# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
