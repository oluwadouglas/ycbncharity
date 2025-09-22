# ASGI config for ycbn_charity project.
import os
from django.core.asgi import get_asgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ycbn_charity.settings')
application = get_asgi_application()
