from django.db import models
from django.conf import settings


class Schedule(models.Model):

    class TransactionType(models.TextChoices):
        INCOME = "INCOME", "입금"
        EXPENSE = "EXPENSE", "출금"

    class RepeatType(models.TextChoices):
        DAILY = "DAILY", "매일"
        WEEKLY = "WEEKLY", "매주"
        MONTHLY = "MONTHLY", "매월"
        YEARLY = "YEARLY", "매년"

    # PK
    schedule_id = models.BigAutoField(primary_key=True)

    # FK
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="schedules",
        db_column="user_id",
    )

    account = models.ForeignKey(
        "account.Account",
        on_delete=models.CASCADE,
        related_name="schedules",
        db_column="account_id",
    )

    category = models.ForeignKey(
        "category.Category",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="schedules",
        db_column="category_id",
    )

    # 기본 정보
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    transaction_type = models.CharField(
        max_length=10,
        choices=TransactionType.choices,
    )

    memo = models.TextField(blank=True)

    repeat_type = models.CharField(
        max_length=10,
        choices=RepeatType.choices,
    )

    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "schedule"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "is_active"]),
            models.Index(fields=["repeat_type"]),
        ]

    def __str__(self):
        return f"{self.title} ({self.repeat_type})"