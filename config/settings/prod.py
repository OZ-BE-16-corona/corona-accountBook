from .base import *  # noqa: F403

DEBUG = False

ALLOWED_HOSTS = ["*"]

CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"
