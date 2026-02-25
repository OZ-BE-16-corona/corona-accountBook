from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            'transaction_id', 'account', 'category', 'amount',
            'currency', 'transaction_type', 'memo', 'transaction_date', 'created_at'
        ]
        read_only_fields = ['transaction_id', 'category', 'created_at']


