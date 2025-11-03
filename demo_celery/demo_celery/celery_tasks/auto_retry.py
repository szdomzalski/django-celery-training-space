from billiard.einfo import ExceptionInfo
from celery import Task
from demo_celery.celery_config import app
import logging


logging.basicConfig(filename='celery_tasks.log', level=logging.ERROR,
                    format='%(asctime)s:%(levelname)s:%(message)s')


# Define a custom task class to handle failures
class MyCustomTask(Task):
    # Override the on_failure method to handle task failures
    def on_failure(self, exc: Exception, task_id: str, args: tuple, kwargs: dict, einfo: ExceptionInfo) -> None:
        logging.error(f"Task {task_id} failed: {exc} args: {args} kwargs: {kwargs}")
        if isinstance(exc, ConnectionError):
            # NOTE: einfo contains the traceback about the exception
            logging.error(f"ConnectionError details: {einfo}")
        else:
            logging.error(f"General error details: {einfo}")


# Set the custom task class as the base task class for the Celery app
app.Task = MyCustomTask


# Specify what exceptions should trigger an automatic retry, auto retry frequency, and max retries
# @app.task(queue='tasks', autoretry_for=(ConnectionError,), default_retry_delay=3, max_retries=3)
@app.task(queue='tasks', autoretry_for=(ConnectionError,), default_retry_delay=3, retry_kwargs={'max_retries': 3})
def my_auto_retry_test() -> None:
    raise ConnectionError("Simulated connection error for auto-retry testing")
