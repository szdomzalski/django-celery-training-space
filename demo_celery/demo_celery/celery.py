import os
import time

from celery import Celery
from celery.app.utils import Settings
from kombu import Exchange, Queue

from consumer.tasks import add2

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demo_celery.settings')

app = Celery('demo_celery')
app.config_from_object('django.conf:settings', namespace='CELERY')
cfg: Settings = app.conf
cfg.task_queues = [
    Queue('tasks', Exchange('tasks'), routing_key='tasks', queue_arguments={'x-max-priority': 10}),
]

cfg.task_acks_late = True  # Acknowledge tasks after they have been executed
cfg.task_default_priority = 5
cfg.worker_prefetch_multiplier = 1  # Limit number of tasks a worker can reserve
cfg.worker_concurrency = 1  # Number of worker processes

# cfg.task_routes = {
#     "consumer.tasks.add": {"queue": "queue_add"},
#     "consumer.tasks.xsum": {"queue": "queue_add"},
#     "consumer.tasks.mul": {"queue": "queue_multiply"},
# }
# cfg.task_default_rate_limit = '1/m'
# cfg.broker_transport_options = {
#     'priority_steps': list(range(10)),
#     'sep': ':',
#     'queue_order_strategy': 'priority',
# }
app.autodiscover_tasks()


# @app.task(bind=True, ignore_result=True)
# def debug_task(self) -> None:
#     print(f'Request: {self.request!r}')

@app.task(queue='tasks')
def sleepy_task_1() -> str:
    time.sleep(3)
    return 'Slept for 3 seconds'


@app.task(queue='tasks')
def sleepy_task_2() -> str:
    time.sleep(3)
    return 'Slept for 3 seconds'


@app.task(queue='tasks')
def sleepy_task_3() -> str:
    time.sleep(3)
    return 'Slept for 3 seconds'


def test() -> None:
    result = add2.apply_async(args=[4, 6], queue='tasks')

    if result.ready():
        print('Task has completed')
    else:
        print('Task is still processing...')

    if result.successful():
        print('Task completed successfully.')
    else:
        print('Task failed.')

    try:
        output = result.get(timeout=10)
        print(f'Task result: {output}')
    except Exception as e:
        print(f'Error retrieving task result: {e}')

    exception = result.get(propagate=False)
    if exception:
        print(f'Task raised an exception: {exception}')


