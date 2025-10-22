import os

from celery import Celery
from celery.app.utils import Settings
from kombu import Exchange, Queue

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

base_dir = os.getcwd()
task_dir = os.path.join(base_dir, 'demo_celery', 'celery_tasks')

if os.path.exists(task_dir) and os.path.isdir(task_dir):
    task_modules = []
    for filename in os.listdir(task_dir):
        if filename.startswith('ex_') and filename.endswith('.py'):
            module_name = f'demo_celery.celery_tasks.{filename[:-3]}'
            # Dynamically import the task module
            # Provides access to the tasks defined in the module
            module = __import__(module_name, fromlist=['*'])
            # Collect all task functions defined in the module
            for name in dir(module):
                # Check if the attribute is a callable task function
                obj = getattr(module, name)
                if callable(obj) and name.startswith('my_task'):
                    # Register the task module for autodiscovery
                    task_modules.append(f'{module_name}.{name}')

    app.autodiscover_tasks(task_modules)
