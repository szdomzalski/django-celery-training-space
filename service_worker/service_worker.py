from datetime import timedelta
import os

from celery import Celery
import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration


sentry_dsn = os.environ['SENTRY_DSN']
sentry_sdk.init(
    dsn=sentry_dsn,
    integrations=[CeleryIntegration()],
)

app = Celery('service_worker')
app.config_from_object('celeryconfig')
# Importing tasks from a separate module; it is required to let Celery know where to find tasks
app.conf.imports = ('app.tasks',)

app.autodiscover_tasks()


app.conf.beat_schedule = {
    'healthcheck': {
        'task': 'app.tasks.check_webpage',
        'schedule': timedelta(seconds=20),
    }
}