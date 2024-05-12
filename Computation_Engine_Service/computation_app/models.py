from django.db import models

class Objective(models.Model):
    value = models.IntegerField()

class Vehicle(models.Model):
    vehicle_id = models.IntegerField()
    route = models.TextField()
    distance = models.IntegerField()

class Maximum(models.Model):
    max_distance = models.IntegerField()
