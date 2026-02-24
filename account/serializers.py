from rest_framework import serializers
from .models import Account

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            'account_id', 'account_name', 'type', 'bank_code', 
            'currency', 'balance', 'is_active', 'created_at'
        ]
        # balance는 거래(Transaction)를 통해서만 변경되어야 하므로 읽기 전용 권장
        read_only_fields = ['account_id', 'balance', 'is_active', 'created_at']