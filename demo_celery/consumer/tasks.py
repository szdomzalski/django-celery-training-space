from celery import shared_task
from django.core.management import call_command
# from numbers import Number
# import time
# from typing import Any, Iterable


@shared_task
def management_command() -> None:
    # Use the name of your management command here as it was called from CLI (i.e. python manage.py <command_name>)
    call_command('test_command')


# Example tasks
# shared_task decorator is used to register tasks when not using the Celery app instance directly
# @shared_task
# def add2(x: Number, y: Number) -> Number:
#     time.sleep(3)
#     return x + y


# # Example of task with rate limit
# @shared_task(rate_limit='5/m')
# def mul2(x: Number, y: Number) -> Number:
#     time.sleep(3)
#     return x * y


# # Example of task with explicit queue assignment
# @shared_task(queue='tasks')
# def xsum(numbers: Iterable[Number]) -> Number:
#     time.sleep(3)
#     return sum(numbers)


# @shared_task
# def echo(value: Any) -> Any:
#     time.sleep(3)
#     return value
