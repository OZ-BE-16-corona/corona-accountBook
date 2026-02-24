from django.db import models


class Category(models.Model):
    class Type(models.TextChoices):
        INCOME = "INCOME", "수입"
        EXPENSE = "EXPENSE", "지출"

    category_name = models.CharField(max_length=50)
    category_type = models.CharField(max_length=10, choices=Type.choices)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "category"
        ordering = ["category_type", "category_name"]
        constraints = [
            # 같은 타입에서 같은 이름 중복 방지 (예: 지출-식비 2개 금지)
            models.UniqueConstraint(
                fields=["category_type", "category_name"],
                name="uniq_category_type_name",
            )
        ]

    def __str__(self) -> str:
        return f"[{self.category_type}] {self.category_name}"