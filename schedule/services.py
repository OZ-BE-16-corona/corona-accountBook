# schedule/services.py
from __future__ import annotations

from config.services.category_classifier import classify_category
from schedule.models import Schedule


def create_schedule(*, user_id: int, account_id: int, title: str, memo: str,
                    amount: int, currency: str, transaction_type: str,
                    repeat_type: str, start_date, end_date,
                    category_id: int | None = None) -> dict:
    text = f"{title} {memo}".strip()

    auto = None
    if not category_id:
        r = classify_category(text)
        category_id = r.category_id
        auto = {
            "category_id": r.category_id,
            "category_name": r.category_name,
            "confidence": r.confidence,
            "matched_keyword": r.matched_keyword,
        }

    sch = Schedule.objects.create(
        user_id=user_id,
        account_id=account_id,
        category_id=category_id,
        title=title,
        memo=memo,
        amount=amount,
        currency=currency,
        transaction_type=transaction_type,
        repeat_type=repeat_type,
        start_date=start_date,
        end_date=end_date,
    )

    resp = {"message": "Schedule Success Create", "schedule_id": sch.id, "category_id": sch.category_id}
    if auto:
        resp["auto_category"] = auto
    return resp