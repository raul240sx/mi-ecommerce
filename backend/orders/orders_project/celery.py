from celery import Celery
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orders_project.settings.local')


app = Celery('orders_project')

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()