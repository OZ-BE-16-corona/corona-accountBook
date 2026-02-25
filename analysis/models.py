from django.db import models
from django.conf import settings
# Create your models here.


class Analysis(models.Model):
    class AboutChoices(models.TextChoices):
        TOTAL_EXPENSE = "TOTAL_EXPENSE", "총 지출"
        TOTAL_INCOME = "TOTAL_INCOME", "총 수입"
        CATEGORY_EXPENSE = "CATEGORY_EXPENSE", "카테고리별 지출"
        CATEGORY_INCOME = "CATEGORY_INCOME", "카테고리별 수입"

    class PeriodTypeChoices(models.TextChoices):
        WEEKLY = "WEEKLY", "매주"
        MONTHLY = "MONTHLY", "매월"
        YEARLY = "YEARLY", "매년"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="analyses"
    )

    about = models.CharField(max_length=30, choices=AboutChoices.choices)

    type = models.CharField(max_length=20, choices=PeriodTypeChoices.choices)

    period_start = models.DateField()
    period_end = models.DateField()

    description = models.TextField()

    result_image = models.ImageField(
        upload_to="analysis_results/", null=True, blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} - {self.about} ({self.period_start} ~ {self.period_end})"
