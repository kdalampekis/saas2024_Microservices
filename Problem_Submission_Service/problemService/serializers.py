from rest_framework import serializers
from .models import *

class MetadataSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    model_id_title = serializers.CharField(source='model_id.title', read_only=True)

    class Meta:
        model = Metadata
        fields = ['submission_id', 'username', 'date', 'credit_cost', 'model_id', 'model_id_title', 'status']

    def get_status(self, obj):
        if obj.is_executed:
            return 'Executed'
        elif obj.is_ready:
            return 'Ready'
        else:
            return 'Not Ready'