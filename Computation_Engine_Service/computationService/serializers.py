from rest_framework import serializers
from .models import VRP

class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VRP
        fields = '__all__'

class NQueensSerializer(serializers.Serializer):
    board_size = serializers.IntegerField(min_value=1)