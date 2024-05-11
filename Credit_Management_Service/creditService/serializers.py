from rest_framework import serializers
from .models import CreditTransaction

class CreditTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditTransaction
        fields = '__all__'
