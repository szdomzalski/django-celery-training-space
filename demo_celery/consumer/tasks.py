from celery import shared_task
from numbers import Number
import time
from typing import Any, Iterable


@shared_task
def add2(x: Number, y: Number) -> Number:
    time.sleep(3)
    return x + y


@shared_task(rate_limit='5/m')
def mul2(x: Number, y: Number) -> Number:
    time.sleep(3)
    return x * y


@shared_task(queue='tasks')
def xsum(numbers: Iterable[Number]) -> Number:
    time.sleep(3)
    return sum(numbers)


@shared_task
def echo(value: Any) -> Any:
    time.sleep(3)
    return value
