from celery import group
from demo_celery.celery_config import app


app.conf.task_acks_late = True  # Acknowledge tasks after they have been executed
# Unacknowledges and rejects tasks if worker is lost or disconnected from broker so it can be reassigned
# Warning - enabling this may lead to increased message requeuing if workers are unstable
app.conf.task_reject_on_worker_lost = True


@app.task(queue='tasks')
def my_task(z: int) -> str | None:
    try:
        if z % 5 == 0:
            raise ValueError(f'Simulated task failure for input: {z}')
    except Exception as e:
        handle_failed_task.apply_async(args=(z, str(e)))
        raise
    return f'Processed value: {z}'


# Dedicated queue for handling failed tasks
@app.task(queue='dead_letter')
def handle_failed_task(z: int, error_message: str) -> None:
    # Here we would normally log the error or send it to a monitoring system
    return f'Task with input {z} failed due to error: {error_message}'


def run_task_group(limit: int = 10) -> None:
    task_group = group(my_task.s(i) for i in range(limit))
    result = task_group.apply_async()
    # print('Task group results:', result.get())
