from celery import chain
from celery.result import AsyncResult
from demo_celery.celery_config import app


@app.task(queue='tasks')
def add(x: int, y: int) -> int:
    return x + y


@app.task(queue='tasks')
def divide(x: int, y: int) -> float:
    if y == 0:
        raise ValueError("Division by zero is not allowed")
    return x / y


def run_chain(x: float, y: float, z: float) -> None:
    task_chain = chain(
        divide.s(x, y),
        add.s(z)
    )
    chain_result: AsyncResult = task_chain.apply_async()
    try:
        result = chain_result.get()
        print(f"Chain completed successfully with result: {result}")
    except Exception as e:
        print(f"Chain failed with exception: {e}")
        raise