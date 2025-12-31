from celery import Celery
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'users_project.settings.local')


app = Celery('users_project')

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()