from django.urls import path
from . import views

urlpatterns = [
    path("<int:account_id>/", views.account_detail),
    path("count/", views.account_count),
]
