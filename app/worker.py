from celery import Celery
from dotenv import load_dotenv
import os

load_dotenv()

celery_app = Celery(
    'tasks',
    broker=os.getenv('BROKER_URL', 'amqp://guest@localhost//'),  # RabbitMQ Broker
    # backend='redis://localhost:6379/0',  # Backend untuk tracking status
    backend=os.getenv('BACKEND_URL','rpc://')
)

celery_app.autodiscover_tasks(['app'])