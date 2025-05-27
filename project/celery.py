import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings
from django.core.cache import cache

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery("project_celery")
app.conf.broker_url = settings.BROKER_URL
app.conf.timezone = os.environ.get('TZ', 'Europe/Bratislava')
app.conf.task_serializer = 'pickle'
app.conf.accept_content = ['json', 'pickle']
app.conf.worker_prefetch_multiplier = 1
app.conf.task_acks_late = True
app.conf.task_time_limit = 1 * 60 * 60
app.conf.worker_max_tasks_per_child = 20

app.conf.ONCE = {
    'backend': 'celery_once.backends.Redis',
    'settings': {
        'url': 'redis://{}:{}'.format(os.environ.get('REDIS_HOST'), os.environ.get('REDIS_PORT')),
        'default_timeout': 60 * 30
    }
}

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()