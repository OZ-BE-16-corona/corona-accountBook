# config/celery.py

import os
from celery import Celery
from celery.schedules import crontab

# ✅ 로컬에서 dev 쓰고 있으니까 이걸로 설정
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")

app = Celery("config")

# settings.py에 정의된 CELERY_ 설정 읽기
app.config_from_object("django.conf:settings", namespace="CELERY")

# analysis/tasks.py 자동 탐색
app.autodiscover_tasks()

# (테스트용) 1분마다 실행
app.conf.beat_schedule = {
    "run-daily-analysis": {
        "task": "analysis.tasks.run_daily_total_expense_analysis",
        "schedule": crontab(minute="*/1"),
    },
}
