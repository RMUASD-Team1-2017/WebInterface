from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from EmergencyUser.forms import DroneDestinationForm
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.urls import reverse
from EmergencyRabbitMQ import rabbit_sender, rabbit_receiver
from EmergencyCommon.models import Drone, DroneMission
from EmergencyRabbitMQ import rabbitSenders
def callback1(ch, method, properties, body):
    print(" [1] Received %r" % body)

def callback2(ch, method, properties, body):
    print(" [2] Received %r" % body)



class DroneDispatch(View):
    def get(self, request, *args, **kwargs):
        template_name = "EmergencyUser/DroneDispatch.html"
        destination_picker = DroneDestinationForm()
        return render(request, template_name, {'destination_picker' : destination_picker, "name" : "bob"} )

    def post(self, request, *args, **kwargs):
        destination_picker = DroneDestinationForm(request.POST)

        if "destination_submit" in request.POST and destination_picker.is_valid():
            lat, lon = tuple(destination_picker.cleaned_data["destination"])
            #Create new mission for this request
            mission = DroneMission(call_longitude = float(lon), call_latitude = float(lat))
            mission.save()
            #rabbitSenders.send_mission_request(mission = mission)

        return HttpResponseRedirect(reverse('EmergencyUser:destination_send', kwargs = {'pk' : mission.id}))

class DroneSend(View):
    def get(self, request, *args, **kwargs):
        template_name = "EmergencyUser/DroneSend.html"
        mission = get_object_or_404(DroneMission, pk = kwargs['pk'])
        return render(request, template_name, {'mission' : mission})

class MissionStatusJSON(View):
    def get(self, request, *args, **kwargs):
        mission = get_object_or_404(DroneMission, pk = kwargs['pk'])
        response = {}
        response['last_update'] = mission.last_update
        response['accepted'] = mission.accepted
        response['goal'] = {'latitude' : mission.goal_latitude, 'longitude' : mission.goal_longitude}
        response['position'] = {'latitude' : None, 'longitude' : None}
        response['eta'] = mission.eta
        response['takeoff_done'] = False
        if mission.the_drone:
            response['position']['latitude'] = mission.the_drone.latitude
            response['position']['longitude'] = mission.the_drone.longitude
            response['takeoff_done'] = True
        return JsonResponse(response)

class MissionStatusView(View):
    def get(self, request, *args, **kwargs):
        mission = get_object_or_404(DroneMission, pk = kwargs['pk'])
        template_name = "EmergencyUser/MissionStatus.html"
        return render(request, template_name, {'mission' : mission})
