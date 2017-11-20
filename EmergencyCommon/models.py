from django.db import models

# Create your models here.


class Drone(models.Model):
    serial = models.CharField(max_length=30)
    latitude = models.FloatField(null = True)
    longitude = models.FloatField(null = True)
    altitude = models.FloatField(null = True)
    #Location reported by OES in case of GCS
    oes_latitude = models.FloatField(null = True)
    oes_longitude = models.FloatField(null = True)
    oes_altitude = models.FloatField(null = True)
    state = models.CharField(max_length=30, null = True)
    last_update = models.DateTimeField(null = True)
    current_mission = models.ForeignKey('DroneMission', null = True, default = None, blank=True)

class DroneHealth(models.Model):
    the_drone = models.ForeignKey(Drone, on_delete = models.CASCADE)

class DroneMission(models.Model):
    the_drone = models.ForeignKey(Drone, on_delete = models.CASCADE, null = True, default = None, blank=True)
    eta = models.DateTimeField(null = True, blank=True)
    start = models.DateTimeField(null = True, default = None, blank=True)
    end = models.DateTimeField(null = True, default = None, blank=True)
    waypoint_longitude = models.FloatField(null = True, blank=True)
    waypoint_latitude = models.FloatField(null = True, blank=True)
    goal_longitude = models.FloatField(null = True, default = None, blank=True)
    goal_latitude = models.FloatField(null = True, default = None, blank=True)
    call_longitude = models.FloatField(null = True, default = None, blank=True)
    call_latitude = models.FloatField(null = True, default = None, blank=True)
    accepted = models.NullBooleanField(default = None, blank=True)
    last_update = models.DateTimeField(null = True, blank=True)


class Waypoint(models.Model):
    mission = models.ForeignKey(DroneMission, on_delete = models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    altitude = models.FloatField(default = 0)
    order = models.IntegerField()

class DronePosition(models.Model):
    the_drone = models.ForeignKey(Drone, on_delete = models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    altitude = models.FloatField()
    time = models.DateTimeField()
