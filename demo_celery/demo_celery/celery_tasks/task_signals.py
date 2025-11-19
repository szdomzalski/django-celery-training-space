from celery.signals import task_failure
from typing import Callable

from demo_celery.celery_config import app


@app.task(queue='tasks')
def cleanup_failed_task(task_id: str, *args, **kwargs) -> None:
    print(f'Cleaning up after failed task {task_id}...', flush=True)
    print(f'Args: {args}, Kwargs: {kwargs}', flush=True)


@app.task(queue='tasks')
def divide(x: float, y: float) -> float:
    return x / y


# Signal handler itself IS NOT a celery task
@task_failure.connect(sender=divide)
def handle_divide_failure(sender: Callable | None = None, task_id: str | None = None, **kwargs) -> None:
    print(f'Task {task_id} sent by {sender} has failed. Triggering cleanup...', flush=True)
    # Expecting kwargs to contain 'signal', 'exception', 'args', 'kwargs', 'einfo'
    print(f'Failure details: {kwargs}', flush=True)
    cleanup_failed_task.delay(task_id)


def run_task(a: int, b: int) -> None:
    divide.apply_async(args=(a, b,))

