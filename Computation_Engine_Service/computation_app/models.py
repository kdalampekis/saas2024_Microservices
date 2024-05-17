from django.db import models

class Results(models.Model):
    name = models.CharField(max_length=200)
    score = models.IntegerField()
    passed = models.BooleanField()
    date = models.DateField()

    def __str__(self):
        return f"{self.name} - {self.score} - {'Passed' if self.passed else 'Failed'}"

class Problems(models.Model):
    objective_id = models.IntegerField()
    number_of_vehicles = models.IntegerField()
    routes = models.TextField()
    maximum_distance = models.IntegerField()

    def __str__(self):
        return f"Objective ID: {self.objective_id}, Vehicles: {self.number_of_vehicles}, Max Distance: {self.maximum_distance}m"

class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}, Age: {self.age}"
