from celery import shared_task
from numbers import Number
from typing import Iterable


@shared_task
def add(x: Number, y: Number) -> Number:
    return x + y


@shared_task
def mul(x: Number, y: Number) -> Number:
    return x * y


@shared_task
def xsum(numbers: Iterable[Number]) -> Number:
    return sum(numbers)