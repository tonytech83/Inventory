from __future__ import unicode_literals, absolute_import
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory.settings')

app = Celery('inventory')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
