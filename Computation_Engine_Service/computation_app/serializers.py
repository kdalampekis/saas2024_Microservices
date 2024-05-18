from rest_framework import serializers
from .models import Problems

class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problems
        fields = '__all__'

class NQueensSerializer(serializers.Serializer):
    board_size = serializers.IntegerField(min_value=1)