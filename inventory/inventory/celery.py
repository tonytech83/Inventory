from __future__ import unicode_literals, absolute_import
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory.settings')

app = Celery('inventory')
app.conf.enable_utc = False
app.conf.update(timezone='Europe/Sofia')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'check-and-send-reports-daily': {
        'task': 'inventory.reports.tasks.check_and_send_reports',
        'schedule': crontab(hour=8, minute=5),
    },
}

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
