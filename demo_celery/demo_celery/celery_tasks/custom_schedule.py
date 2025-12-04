from datetime import timedelta

from celery.schedules import crontab

from demo_celery.celery_config import app

a = 0
b = 1
c = 1
d = 2

# app.conf.beat_schedule = {
#     'add': {
#         'task': 'demo_celery.celery_tasks.custom_schedule.add',
#         'schedule': crontab(),  # Executes every minute
#     },
#     'multiply': {
#         'task': 'demo_celery.celery_tasks.custom_schedule.multiply',
#         'schedule': timedelta(seconds=10),
#         'kwargs': {'foo': 'bar'},
#         'args': (1, 2),  # Unfortunately, passed args cannot be changed dynamically (fixed at startup time)
#         'options': {
#             'queue': 'tasks',
#             'priority': 5,
#         }
#     },
# }


@app.task(queue='tasks')
def multiply(a: int, b: int, **kwargs) -> float:
    print(f'Multiplying {a} and {b}')
    print(f'kwargs: {kwargs}')
    return a * b


@app.task(queue='tasks')
def add() -> float:
    global a, b
    print(f'Adding {a} and {b}')
    tmp = a + b
    a = b
    b = tmp
    return tmp