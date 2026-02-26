from .base import *  # noqa: F403


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # 또는 지정하고 싶은 경로

DEBUG = False

ALLOWED_HOSTS = ["*"]

CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"

