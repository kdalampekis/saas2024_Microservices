from rest_framework import serializers
from .models import *

class InputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Input
        fields = ['metadata', 'input_file', 'input_data']

class MetadataSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    model_id_title = serializers.CharField(source='model_id.title', read_only=True)

    class Meta:
        model = Metadata
        fields = ['submission_id', 'username', 'date', 'credit_cost', 'model_id', 'model_id_title', 'status']

    def get_status(self, obj):
        if obj.is_ready:
            return 'Ready'
        elif obj.is_executed:
            return 'Executed'
        else:
            return 'Not Executed'
