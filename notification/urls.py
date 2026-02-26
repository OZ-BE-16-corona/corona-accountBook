from django.urls import path
from .views import UnreadNotificationListView, NotificationReadView

urlpatterns = [
    path(
        "notifications/unread/",
        UnreadNotificationListView.as_view(),
        name="notification-unread-list",
    ),
    path(
        "notifications/<int:notification_id>/read/",
        NotificationReadView.as_view(),
        name="notification-read",
    ),
]
