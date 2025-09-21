from celery import Celery

app = Celery('celery_standalone')
app.config_from_object('celeryconfig')
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self) -> None:
    print(f'Request: {self.request!r}')
