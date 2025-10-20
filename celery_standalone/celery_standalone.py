from celery import Celery

app = Celery('celery_standalone')
app.config_from_object('celeryconfig')
# Importing tasks from a separate module; it is required to let Celery know where to find tasks
app.conf.imports = ('consumer.tasks',)

app.autodiscover_tasks()

# Debug task prepared for testing worker setup and connectivity
# @app.task(bind=True, ignore_result=True)
# def debug_task(self) -> None:
#     print(f'Request: {self.request!r}')
