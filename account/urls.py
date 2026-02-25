from django.urls import path
from . import views

urlpatterns = [
    path("<int:account_id>/", views.account_detail),
    path("count/", views.account_count),
]
from .views import AccountListCreateView, AccountDetailDeleteView

app_name = 'account'

urlpatterns = [
    path('account/', AccountListCreateView.as_view(), name='account-list-create'),
    path('account/<int:pk>/', AccountDetailDeleteView.as_view(), name='account-detail-delete'),
]
