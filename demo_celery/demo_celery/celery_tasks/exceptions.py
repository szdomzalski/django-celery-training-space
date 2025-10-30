from demo_celery.celery_config import app
import logging


logging.basicConfig(filename='celery_tasks.log', level=logging.ERROR,
                    format='%(asctime)s:%(levelname)s:%(message)s')


# @app.task(queue='tasks')
# def my_task_test_1(name: str) -> str:
#     pass


# @app.task(queue='tasks')
# def my_task_test_2(name: str) -> str:
#     pass


@app.task(queue='tasks')
def my_task_exception_test():
    try:
        raise ConnectionError("Simulated connection error for testing")
    except Exception as e:
        logging.error(f"An error occurred in my_task_test_3: {e}")
        raise  # This will ensure the task is marked as failed in Celery