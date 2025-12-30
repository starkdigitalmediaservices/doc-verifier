import os
from celery import Celery

# Read Celery settings from environment (minimal dependencies)
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/1")

celery_app = Celery(
    "worker",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
    include=['api.routes.tasks'],  # Add task modules here (e.g., 'api.routes.tasks', 'core.tasks')
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
)

# Create alias for easy import: from core.celery import _celery
_celery = celery_app

# Import task modules to ensure tasks are registered
# This is necessary because autodiscover_tasks() may not find tasks
# if the modules aren't imported when Celery starts
import api.routes.verification  # noqa: F401

celery_app.autodiscover_tasks()
