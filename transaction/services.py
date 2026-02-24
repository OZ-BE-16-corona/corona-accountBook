# transaction/services.py
from __future__ import annotations

from config.services.category_classifier import classify_category
from transaction.models import Transaction


def create_transaction(*, user_id: int, account_id: int, amount: int, currency: str,
                       transaction_type: str, memo: str, transaction_date,
                       category_id: int | None = None) -> dict:
    """
    category_id가 없으면 memo로 자동 분류해서 저장
    """
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
        "transaction_id": tx.id,
        "category_id": tx.category_id,
    }
    if auto:
        resp["auto_category"] = auto
    return resp