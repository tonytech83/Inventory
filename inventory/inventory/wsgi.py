import os

from django.core.wsgi import get_wsgi_application

settings_module = 'inventory.deployment' if 'WEBSITE_HOST' in os.environ else 'inventory.settings'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

application = get_wsgi_application()
