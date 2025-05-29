from django.apps import AppConfig


class SyncConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "project.sync"

    def ready(self):
        from .celery import register_celery_tasks

        register_celery_tasks()