from celery import shared_task
from numbers import Number
import time
from typing import Any, Iterable


@shared_task
def add2(x: Number, y: Number, queue: str = 'celery') -> Number:
    time.sleep(3)
    return x + y


@shared_task(rate_limit='5/m')
def mul2(x: Number, y: Number, queue: str = 'celery:0') -> Number:
    time.sleep(3)
    return x * y


@shared_task
def xsum(numbers: Iterable[Number], queue: str = 'celery:1') -> Number:
    time.sleep(3)
    return sum(numbers)


@shared_task
def echo(value: Any, queue: str = 'celery:2') -> Any:
    time.sleep(3)
    return value
