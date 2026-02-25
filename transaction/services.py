from __future__ import annotations
from django.db import transaction as db_transaction
from rest_framework.exceptions import ValidationError
from account.models import Account
from config.services.category_classifier import classify_category
from .models import Transaction


def create_transaction(*, user_id: int, account_id: int, amount: int, currency: str,
                       transaction_type: str, memo: str, transaction_date,
                       category_id: int | None = None) -> dict:
    auto = None

    if not category_id:
        r = classify_category(memo)
        category_id = r.category_id
        auto = {
            "category_id": r.category_id,
            "category_name": r.category_name,
            "confidence": r.confidence,
            "matched_keyword": r.matched_keyword,
        }

    with db_transaction.atomic():
        account = Account.objects.select_for_update().get(pk=account_id, user_id=user_id)

        if transaction_type == Transaction.TransactionType.EXPENSE:
            if account.balance < amount:
                raise ValidationError("잔액이 부족합니다.")
            account.balance -= amount
        else:  # INCOME
            account.balance += amount

        account.save()

        tx = Transaction.objects.create(
            user_id=user_id,
            account_id=account_id,
            category_id=category_id,
            amount=amount,
            currency=currency,
            transaction_type=transaction_type,
            memo=memo,
            transaction_date=transaction_date,
        )

    resp = {
        "message": "Transaction Success Create",
        "transaction_id": tx.transaction_id,  # 모델 필드명에 맞춤
        "category_id": tx.category_id,
        "current_balance": account.balance  # 현재 잔액 반환 추가
    }

    if auto:
        resp["auto_category"] = auto
    return resp