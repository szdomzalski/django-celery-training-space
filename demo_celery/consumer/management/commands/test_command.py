from typing import Any

from django.core.management.base import BaseCommand


# It MUST BE named Command; this is how Django manage.py recognizes it as a management command
class Command(BaseCommand):
    help = 'A test command that prints a message'

    def handle(self, *args: Any, **options: Any) -> None:
        print('This is my simple test command')