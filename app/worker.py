from celery import Celery


celery_app = Celery(
    'tasks',
    broker='amqp://guest@localhost//',  # RabbitMQ Broker
    backend='rpc://',  # Backend untuk tracking status
)
