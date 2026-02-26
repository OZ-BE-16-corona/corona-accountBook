from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Notification
from .serializers import NotificationSerializer


# ✅ mission_1: 요청 유저의 "읽지 않은 알림" 리스트
class UnreadNotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(
            user=self.request.user, is_read=False
        ).order_by("-created_at")


# ✅ mission_2: 알림 읽음 처리 (pk로 받기)
class NotificationReadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, notification_id: int):
        notif = get_object_or_404(
            Notification,
            notification_id=notification_id,
            user=request.user,
        )

        if not notif.is_read:
            notif.is_read = True
            notif.read_at = timezone.now()
            notif.save(update_fields=["is_read", "read_at", "updated_at"])

        return Response(
            {
                "message": "알림을 읽음 처리했습니다.",
                "notification_id": notif.notification_id,
                "is_read": notif.is_read,
                "read_at": notif.read_at,
            },
            status=status.HTTP_200_OK,
        )
