from .base import *  # noqa: F403
from .base import BASE_DIR

STATIC_ROOT = BASE_DIR / 'staticfiles'

DEBUG = False

ALLOWED_HOSTS = ["*"]

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"

