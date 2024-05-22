from rest_framework import serializers
from .models import CreditTransaction, UserCreditBalance

class CreditTransactionSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()

    class Meta:
        model = CreditTransaction
        fields = ['user_id', 'credits', 'created_at']
        read_only_fields = ['created_at']

class UserCreditBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCreditBalance
        fields = ['user_id', 'balance']
