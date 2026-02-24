from rest_framework import serializers
from .models import Account

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            'account_id', 'account_name', 'type', 'bank_code', 
            'currency', 'balance', 'is_active', 'created_at'
        ]

        read_only_fields = ['account_id', 'balance', 'is_active', 'created_at']