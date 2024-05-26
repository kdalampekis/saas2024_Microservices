from django.db import models


# Seperate model for vrp problems
class VRP(models.Model):
    objective_id = models.IntegerField()
    number_of_vehicles = models.IntegerField()
    routes = models.TextField()
    maximum_distance = models.IntegerField()

    def __str__(self):
        return f"Objective ID: {self.objective_id}, Vehicles: {self.number_of_vehicles}, Max Distance: {self.maximum_distance}m"

class Results(models.Model):
    problem_name = models.CharField(max_length=100)
    response_data = models.JSONField()
    time_taken = models.FloatField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.problem_name
