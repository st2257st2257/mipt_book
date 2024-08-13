import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'emailservice.settings')
app = Celery('emailservice')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'get_categories_every_one_minutes': {
        'task': 'emailservice.send_weekly',
        'schedule': 30.0
    },
}

app.conf.beat_schedule = {
    'get_categories_every_one_minutes': {
        'task': 'tasks.send_weekly',
        'schedule': crontab(minute='*/1')
    },
}
