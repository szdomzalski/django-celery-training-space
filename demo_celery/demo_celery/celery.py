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

# Setting up a priority queue with RabbitMQ broker
cfg.task_queues = [
    Queue('tasks', Exchange('tasks'), routing_key='tasks', queue_arguments={'x-max-priority': 10}),
]

# Setting up task acknowledgment, priority, and worker concurrency with RabbitMQ broker
cfg.task_acks_late = True  # Acknowledge tasks after they have been executed
cfg.task_default_priority = 5
cfg.worker_prefetch_multiplier = 1  # Limit number of tasks a worker can reserve
cfg.worker_concurrency = 1  # Number of worker processes

# Example of task routing into different queues with rate limiting; prioritization concept with Redis broker
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

# Automatically discover tasks from installed Django apps
app.autodiscover_tasks()


# Debug task prepared for testing worker setup and connectivity
# @app.task(bind=True, ignore_result=True)
# def debug_task(self) -> None:
#     print(f'Request: {self.request!r}')


# Example tasks
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
    # Dispatch the task asynchronously
    result = add2.apply_async(args=[4, 6], queue='tasks')

    # Check if the task is ready to collect the result
    if result.ready():
        print('Task has completed')
    else:
        print('Task is still processing...')

    # Check if the task completed successfully
    if result.successful():
        print('Task completed successfully.')
    else:
        print('Task failed.')

    # Wait for the task to complete and get the result
    try:
        output = result.get(timeout=10)
        print(f'Task result: {output}')
    except Exception as e:
        print(f'Error retrieving task result: {e}')

    # Check for exceptions without raising them
    exception = result.get(propagate=False)
    if exception:
        print(f'Task raised an exception: {exception}')


# Synchronous vs Asynchronous Execution Examples
def execute_sync() -> None:
    result = add2.apply_async(args=[4, 6], queue='tasks')
    task_result = result.get()
    print(f'Task result: {task_result}')
    print('result.get caught the main thread until the task is finished')


def execute_async() -> None:
    result = add2.apply_async(args=[6, 7], queue='tasks')
    print('Task has been dispatched, main thread is free to continue doing other work.')
    print('Doing other work...')
