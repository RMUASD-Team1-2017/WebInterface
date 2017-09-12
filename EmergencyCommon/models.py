from django.db import models

# Create your models here.

class Drone(models.Model):
    serial = models.CharField(max_length=30)
    latitude = models.FloatField(null = True)
    longtitude = models.FloatField(null = True)
    eta = models.DateTimeField(null = True)
    state = models.CharField(max_length=30, null = True)
    last_update = models.DateTimeField(null = True)
    goal_longtitude = models.FloatField(null = True)
    goal_latitude = models.FloatField(null = True)
    waypoint_longtitude = models.FloatField(null = True)
    waypoint_latitude = models.FloatField(null = True)

class DroneHealth(models.Model):
    drone = models.ForeignKey(Drone, on_delete = models.CASCADE)

class DroneMission(models.Model):
    drone = models.ForeignKey(Drone, on_delete = models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()

class DronePosition(models.Model):
    drone = models.ForeignKey(Drone, on_delete = models.CASCADE)
    latitude = models.FloatField()
    longtitude = models.FloatField()
    time = models.DateTimeField()
