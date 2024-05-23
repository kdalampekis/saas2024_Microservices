from rest_framework import serializers
from .models import Metadata

class MetadataSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    problem_type_title = serializers.CharField(source='problem_type.title', read_only=True)

    class Meta:
        model = Metadata
        fields = ['submission_id', 'user', 'username', 'date', 'credit_cost', 'problem_type_title', 'status']

    def get_status(self, obj):
        if obj.is_executed:
            return 'Executed'
        elif obj.is_ready:
            return 'Ready'
        else:
            return 'Not Ready'