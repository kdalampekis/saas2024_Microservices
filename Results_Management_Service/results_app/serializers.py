from rest_framework import serializers

class ProblemsDeserializer(serializers.Serializer):
    id = serializers.IntegerField()
    objective_id = serializers.IntegerField()
    number_of_vehicles = serializers.IntegerField()
    routes = serializers.CharField()  # Use CharField for text data
    maximum_distance = serializers.IntegerField()
