# analysis/tasks.py
from __future__ import annotations

from datetime import date, timedelta

from celery import shared_task
from django.contrib.auth import get_user_model

from analysis.services import AnalysisService


@shared_task
def run_daily_total_expense_analysis():
    """
    매일(또는 스케줄에 따라) 전체 유저의 '전일 총지출' 분석을 생성하는 예시 Task.
    """
    User = get_user_model()

    yesterday = date.today() - timedelta(days=1)

    for user in User.objects.all().iterator():
        AnalysisService.create_analysis(
            user=user,
            about="TOTAL_EXPENSE",
            type="DAILY",
            period_start=yesterday,
            period_end=yesterday,
            description=f"Auto daily expense analysis for {yesterday}",
        )
