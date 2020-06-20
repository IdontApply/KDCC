from celery import Celery
import requests

celery = Celery
celery.config_from_object('celeryconfig')
