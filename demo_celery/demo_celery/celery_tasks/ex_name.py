from demo_celery.celery_config import app


@app.task(queue='tasks')
def my_task_test_1(name: str) -> str:
    pass


@app.task(queue='tasks')
def my_task_test_2(name: str) -> str:
    pass