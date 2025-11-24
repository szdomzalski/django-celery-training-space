from sentry_sdk import capture_exception

from demo_celery.celery_config import app


@app.task(queue='tasks')
def divide(x: int, y: int) -> float:
    try:
        result = x / y
        return result
    except ZeroDivisionError as e:
        # capture_exception(e)
        raise
