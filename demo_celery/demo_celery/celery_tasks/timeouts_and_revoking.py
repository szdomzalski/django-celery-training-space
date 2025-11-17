from encodings.punycode import T

from demo_celery.celery_config import app
from time import sleep



# Task has to be processed within 5 seconds, otherwise it will raise TimeLimitExceeded exception and fail (hard limit)
@app.task(time_limit=10, queue='tasks')
def long_running_task(duration: int) -> str:
    sleep(duration)
    return f'Task completed after sleeping for {duration} seconds'


def execute_timeout_example() -> None:
    result = long_running_task.delay(6)
    try:
        task_result = result.get(timeout=4)
    except TimeoutError:
        # It won't be revoked as it would be for a time limit.
        # The task will still complete after 6 seconds but we won't wait for it here
        print('Task timed out.')
    else:
        print(f'Task result: {task_result}')


def execute_manual_revoke_example() -> None:
    result = long_running_task.delay(6)
    # result.revoke()  # Revoke the task before it starts processing; it might be executed if already started
    result.revoke(terminate=True)  # Forcefully terminate the task even if it's already running
    print(result.status)  # Probably 'PENDING' as revocation is not immediate (and not blocking)
    sleep(1)
    print(result.status)  # Expect 'REVOKED'


def execute_time_limit_example():
    result = long_running_task.delay(12)  # This will exceed the time limit of 10 seconds and task will fail
    try:
        task_result = result.get()
    except Exception as e:
        print(f'Task failed due to: {e}')
    else:
        print(f'Task result: {task_result}')
