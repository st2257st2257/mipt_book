import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
app = Celery('backend')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'start_pair_1': {
        'task': 'main.tasks.update_audience_regular',
        'schedule': crontab(hour=9, minute=0),
        'args': (1,),
    },
    'start_pair_2': {
        'task': 'main.tasks.update_audience_regular',
        'schedule': crontab(hour=10, minute=45),
        'args': (2,),
    },
    'start_pair_3': {
        'task': 'main.tasks.update_audience_regular',
        'schedule': crontab(hour=12, minute=20),
        'args': (3,),
    },
    'start_pair_4': {
        'task': 'main.tasks.update_audience_regular',
        'schedule': crontab(hour=13, minute=55),
        'args': (4,),
    },
    'start_pair_5': {
        'task': 'main.tasks.update_audience_regular',
        'schedule': crontab(hour=15, minute=30),
        'args': (5,),
    },
    'start_pair_6': {
        'task': 'main.tasks.update_audience_regular',
        'schedule': crontab(hour=17, minute=5),
        'args': (6,),
    },
    'start_pair_7': {
        'task': 'main.tasks.update_audience_regular',
        'schedule': crontab(hour=18, minute=35),
        'args': (7,),
    },
    'start_pair_8': {
        'task': 'main.tasks.update_audience_regular',
        'schedule': crontab(hour=20, minute=0),
        'args': (8,),
    },
    'start_pair_9': {
        'task': 'main.tasks.update_audience_regular',
        'schedule': crontab(hour=22, minute=0),
        'args': (9,),
    },
    'start_pair_10': {
        'task': 'main.tasks.update_audience_regular',
        'schedule': crontab(hour=23, minute=59),
        'args': (10,),
    },
    'start_pair_11': {
        'task': 'main.tasks.update_audience_regular',
        'schedule': crontab(hour=1, minute=30),
        'args': (11,),
    },
    'start_pair_12': {
        'task': 'main.tasks.update_audience_regular',
        'schedule': crontab(hour=3, minute=0),
        'args': (12,),
    },
    'start_pair_13': {
        'task': 'main.tasks.update_audience_regular',
        'schedule': crontab(hour=4, minute=30),
        'args': (13,),
    },
    'start_pair_14': {
        'task': 'main.tasks.update_audience_regular',
        'schedule': crontab(hour=6, minute=00),
        'args': (14,),
    },
    'test_1': {
        'task': 'main.tasks.update_audience_regular',
        'schedule': crontab(hour=23, minute=53),
        'args': (1,),
    },
    'test_2': {
        'task': 'main.tasks.update_audience_regular',
        'schedule': crontab(day_of_week=1, hour=11, minute=34),
        'args': (2,),
    },
    'test_3': {
        'task': 'main.tasks.update_week_day',
        'schedule': crontab(day_of_week=1, hour=11, minute=33),
        'args': (1,),
    },
    'update_week_1': {  # Обновляем понедельник
        'task': 'main.tasks.update_week_day',
        'schedule': crontab(day_of_week=0, hour=8, minute=0),
        'args': (1,),
    },
    'update_week_2': {  # Обновляем вторник
        'task': 'main.tasks.update_week_day',
        'schedule': crontab(day_of_week=1, hour=8, minute=0),
        'args': (2,),
    },
    'update_week_3': {  # Обновляем среду
        'task': 'main.tasks.update_week_day',
        'schedule': crontab(day_of_week=2, hour=8, minute=0),
        'args': (3,),
    },
    'update_week_4': {  # Обновляем четверг
        'task': 'main.tasks.update_week_day',
        'schedule': crontab(day_of_week=3, hour=8, minute=0),
        'args': (4,),
    },
    'update_week_5': {  # Обновляем пятницу
        'task': 'main.tasks.update_week_day',
        'schedule': crontab(day_of_week=4, hour=8, minute=0),
        'args': (5,),
    },
    'update_week_6': {  # Обновляем субботу
        'task': 'main.tasks.update_week_day',
        'schedule': crontab(day_of_week=5, hour=8, minute=0),
        'args': (6,),
    },
    'update_week_7': {  # Обновляем воскресенье
        'task': 'main.tasks.update_week_day',
        'schedule': crontab(day_of_week=6, hour=8, minute=0),
        'args': (0,),
    },

}

app.conf.timezone = 'Europe/Moscow'
