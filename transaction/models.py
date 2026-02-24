from django.conf import settings
from django.db import models


class Transaction(models.Model):

    class TransactionType(models.TextChoices):
        INCOME = "INCOME", "입금"
        EXPENSE = "EXPENSE", "출금"

    transaction_id = models.BigAutoField(primary_key=True)

    # 관계
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="transactions"
    )

    account = models.ForeignKey(
        "accounts.Account",
        on_delete=models.CASCADE,
        related_name="transactions"
    )

    category = models.ForeignKey(
        "categories.Category",
        on_delete=models.PROTECT,
        related_name="transactions"
    )

    # 거래 정보
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.CharField(max_length=10, default="KRW")

    transaction_type = models.CharField(
        max_length=10,
        choices=TransactionType.choices
    )

    memo = models.TextField(blank=True, null=True)
    transaction_date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "transaction"
        ordering = ["-transaction_date", "-created_at"]

    def __str__(self):
        return f"{self.transaction_date} | {self.amount} | {self.transaction_type}"