# WSGI config for ycbn_charity project.
import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ycbn_charity.settings')
application = get_wsgi_application()
