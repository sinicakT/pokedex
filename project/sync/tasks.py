from project.celery import app
from django.core.management import call_command


@app.task(name='daily_sync_all')
def daily_sync_all():
    print("Running management command: sync_all")
    try:
        call_command("sync_all")
        print("✓ sync_all completed successfully")
    except Exception as e:
        print(f"✗ sync_all failed: {e}")
