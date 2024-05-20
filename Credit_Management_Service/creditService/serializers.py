from rest_framework import serializers
from .models import CreditTransaction, UserCreditBalance
from django.contrib.auth.models import User

class CreditTransactionSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = CreditTransaction
        fields = ['user', 'credits']

class UserCreditBalanceSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = UserCreditBalance
        fields = ['user', 'balance']
