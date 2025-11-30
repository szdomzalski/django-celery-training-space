from datetime import timedelta

from demo_celery.celery_config import app

a = 0
b = 1
c = 1
d = 2

app.conf.beat_schedule = {
    'add': {
        'task': 'demo_celery.celery_tasks.task_scheduling.add',
        'schedule': timedelta(seconds=10),
    },
    'multiply': {
        'task': 'demo_celery.celery_tasks.task_scheduling.mutliply',
        'schedule': timedelta(seconds=10),
    }
}


@app.task(queue='tasks')
def mutliply() -> float:
    global c, d
    print(f'Multiplying {c} and {d}')
    tmp = c * d
    c = d
    d = tmp
    return d


@app.task(queue='tasks')
def add() -> float:
    global a, b
    print(f'Adding {a} and {b}')
    tmp = a + b
    a = b
    b = tmp
    return tmp