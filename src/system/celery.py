import os
import django
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "finance.settings")

# Ensure Django is fully initialized before importing models
django.setup()

from finance.tasks_base import BaseTaskWithMeta  # Import AFTER django.setup()

app = Celery("finance")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

# Set custom base task
app.Task = BaseTaskWithMeta
