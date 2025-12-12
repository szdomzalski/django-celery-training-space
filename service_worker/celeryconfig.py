# Celery Configuration for standalone Celery worker using Redis
broker_url = 'amqp://guest:guest@broker:5672/'
result_backend = 'rpc://'