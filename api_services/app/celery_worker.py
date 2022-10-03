from celery import Celery
from settings import config
from kombu import Connection
import socket

celery_execute = Celery(broker=config.REDIS_queue, backend=config.REDIS_backend)
