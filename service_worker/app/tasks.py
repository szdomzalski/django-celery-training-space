import os

from celery import shared_task
import requests
from sentry_sdk import capture_exception


PRODUCER_HOST = os.environ.get("PRODUCER_HOST", "django-producer")
PRODUCER_PORT = os.environ.get("PRODUCER_PORT", "8000")
PRODUCER_URL = f"http://{PRODUCER_HOST}:{PRODUCER_PORT}"


@shared_task
def check_webpage() -> None:
    print("Checking webpage...")
    try:
        response = requests.get('http://django-producer:8000')
        response.raise_for_status()
        print(f"Webpage is up! Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print("An error occurred while checking the webpage.")
        capture_exception(e)
    except requests.HTTPError:
        print("Webpage is down!")
        raise
