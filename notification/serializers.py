from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            "notification_id",
            "title",
            "content",
            "notification_type",
            "is_read",
            "read_at",
            "created_at",
            "updated_at",
            "user_id",  # FK id만 내려주고 싶을 때
        ]
        read_only_fields = [
            "notification_id",
            "is_read",
            "read_at",
            "created_at",
            "updated_at",
        ]
