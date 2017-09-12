from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Drone)
admin.site.register(DroneHealth)
admin.site.register(DroneMission)
admin.site.register(DronePosition)
