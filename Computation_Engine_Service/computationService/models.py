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
    submission_id = models.IntegerField(help_text="Unique identifier for the submission")
    problem_name = models.CharField(max_length=100, help_text="Name of the problem solved")
    response_data = models.JSONField(help_text="The response data from the computation")
    time_taken = models.FloatField(null=True, help_text="Time taken to solve the problem in seconds")
    timestamp = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the result was recorded")

    def __str__(self):
        return self.problem_name
