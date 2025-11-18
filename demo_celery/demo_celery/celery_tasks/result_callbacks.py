from celery.app.task import Context

from demo_celery.celery_config import app


@app.task(queue='tasks')
def divide(x: float, y: float) -> float:
    try:
        return x / y
    except ZeroDivisionError as e:
        raise ValueError("I messed up!") from e


@app.task(queue='tasks')
def process_task_result(result: float) -> None:
    print(f'Processing task result {{{result}}}...', flush=True)


# That handler will not be processed as celery task; tool to implement notifications, error logging etc.
@app.task(queue='tasks')
def error_handler(task_ctx: Context, exc: Exception, traceback: str) -> None:
    print(f'Handling error for task {task_ctx}: {exc}', flush=True)
    print(f'Traceback: {traceback}', flush=True)


def run_task_success_callback(a: int, b: int) -> None:
    divide.apply_async(args=(a, b,), link=[process_task_result.s(),])  # Example of callback for success result


def run_task_success_and_error_callback(a: int, b: int) -> None:
    divide.apply_async(
        args=(a, b,),
        link=[process_task_result.s(),],  # Callback for success result
        link_error=[error_handler.s(),],  # Callback for error result
    )
