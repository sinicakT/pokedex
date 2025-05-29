from celery.schedules import crontab

from project.celery import *


def register_celery_tasks():
    app.conf.beat_schedule.update({
        'daily_sync_all': {
            'task': 'daily_sync_all',
            'schedule': crontab(hour=3, minute=0)
        },
    })
