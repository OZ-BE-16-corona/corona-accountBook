from django.db import models
from django.conf import settings


class Notification(models.Model):
    class NotificationType(models.TextChoices):
        PAYMENT = "PAYMENT", "결제 알림"
        NOTICE = "NOTICE", "공지사항"
        SYSTEM = "SYSTEM", "시스템"
        ETC = "ETC", "기타"

    # ERD: notification_id (PK)
    notification_id = models.BigAutoField(primary_key=True)

    # ERD: user_id (FK) - 알림 수신 대상자
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
        db_column="user_id",
    )

    # ERD: title / content
    title = models.CharField(max_length=100)
    content = models.TextField()

    # ERD: notification_type
    notification_type = models.CharField(
        max_length=20,
        choices=NotificationType.choices,
        default=NotificationType.SYSTEM,
    )

    # ERD: is_read / read_at
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

    # ERD: created_at / updated_at
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "notification"
        indexes = [
            models.Index(fields=["user", "is_read", "created_at"]),
            models.Index(fields=["notification_type", "created_at"]),
        ]

    def __str__(self) -> str:
        return f"[{self.notification_type}] {self.title}"