from django.conf import settings
from django.db import models


class Account(models.Model):
    # ERD: account_id (PK, BIGINT)
    account_id = models.BigAutoField(primary_key=True)

    # ERD: account_name VARCHAR(20)
    account_name = models.CharField(max_length=20)

    # ERD: type VARCHAR(20)
    # (ERD에 값 정의가 없어서 일단 문자열로 두고, 나중에 choices로 고정해도 됨)
    type = models.CharField(max_length=20)

    # ERD: bank_code CHAR(3)
    bank_code = models.CharField(max_length=3)

    # ERD: currency CHAR(3)
    currency = models.CharField(max_length=3)

    # ERD: balance BIGINT
    balance = models.BigIntegerField(default=0)

    # ERD: is_active BOOLEAN
    is_active = models.BooleanField(default=True)

    # ERD: created_at / updated_at DATETIME
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ERD: user_id (FK -> User.user_id)
    # 커스텀 유저든 기본 유저든 안전하게 AUTH_USER_MODEL로 연결
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="accounts",
        db_column="user_id",
    )

    class Meta:
        db_table = "account"
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self) -> str:
        return f"{self.account_name} ({self.currency})"