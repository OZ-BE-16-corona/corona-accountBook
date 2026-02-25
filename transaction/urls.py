from django.urls import path
from .views import TransactionListCreateView, TransactionDetailView

app_name = 'transaction'

urlpatterns = [
    path('transaction/', TransactionListCreateView.as_view(), name='transaction-list'),
    path('transaction/<int:pk>/', TransactionDetailView.as_view(), name='transaction-detail'),
]