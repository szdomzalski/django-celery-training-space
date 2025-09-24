import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demo_celery.settings')

app = Celery('demo_celery')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.task_routes = {'consumer.tasks.add': {'queue': 'queue_add'},
                        'consumer.tasks.xsum': {'queue': 'queue_add'},
                        'consumer.tasks.mul': {'queue': 'queue_multiply'},}
app.autodiscover_tasks()


# @app.task(bind=True, ignore_result=True)
# def debug_task(self) -> None:
#     print(f'Request: {self.request!r}')
