from .base import *  # noqa: F403
from .base import BASE_DIR

STATIC_ROOT = BASE_DIR / 'staticfiles'

DEBUG = True

ALLOWED_HOSTS = ["*"]

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
