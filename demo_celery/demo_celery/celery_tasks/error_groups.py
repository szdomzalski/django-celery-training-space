from celery import group
from celery.result import AsyncResult
from demo_celery.celery_config import app


@app.task(queue='tasks')
def my_task(x: int, y: int) -> int:
    if y == 0:
        raise ValueError("Division by zero is not allowed")
    return x // y


def handle_result(result: AsyncResult) -> None:
    if result.successful():
        print(f"Task completed successfully with result: {result.get()}")
    elif result.failed():
        print(f"Task failed with exception: {result.result}")
    elif result.status == 'REVOKED':
        print(f"Task {{{result.id}}} was revoked before execution")


def run_tasks() -> None:
    task_group = group(
        my_task.s(10, 2),
        my_task.s(10, 0),  # This will raise an exception
        my_task.s(10, 5),
        my_task.s(5, 0),   # This will also raise an exception
        my_task.s(20, 4)
    )
    group_result = task_group.apply_async()
    # Retrieve results of the task group execution in the blocking manner
    # We set disable_sync_subtasks to False to enable retrieval of individual tasks not just only the group result
    # We set propagate to False to suppress exceptions in individual tasks from being propagated here
    group_result.get(disable_sync_subtasks=False, propagate=False)

    for result in group_result:
        handle_result(result)