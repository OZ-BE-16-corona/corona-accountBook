from django.urls import path
from .views import (
    UnreadNotificationListView,
    NotificationReadView,
    NotificationListCreateView,
    NotificationDetailDeleteView,
)

urlpatterns = [
    path(
        "notification/unread/",
        UnreadNotificationListView.as_view(),
        name="notification-unread-list",
    ),
    path(
        "notification/<int:notification_id>/read/",
        NotificationReadView.as_view(),
        name="notification-read",
    ),
    path(
        "notification/",
        NotificationListCreateView.as_view(),
        name="notification-list-create",
    ),
    path(
        "notification/<int:pk>/",
        NotificationDetailDeleteView.as_view(),
        name="notification-detail-delete",
    ),
]
