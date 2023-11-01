import os

from celery import Celery
from celery.schedules import crontab

from exchange.tasks import pull_rate

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'celery_periodic_tasks.settings')

app = Celery('celery_periodic_tasks')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 1 seconds.
    sender.add_periodic_task(10.0, pull_rate, name='add every 10')


# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "add-every-midnight": {
        "task": "exchange.tasks.pull_rate",
        "schedule": crontab(minute='0', hour='0'),
    },
}
