from django.shortcuts import render
from django.views.generic import View
from EmergencyUser.forms import DroneDestinationForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from EmergencyRabbitMQ import rabbit_sender, rabbit_receiver

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
            destination = destination_picker.cleaned_data["destination"]
            print("Sending drone to Latitude {}, Longitude {}".format(destination[0], destination[1]))
        return HttpResponseRedirect(reverse('EmergencyUser:destination_send', kwargs = {'lat' : str(destination[0]), 'lon' : str(destination[1])}))

class DroneSend(View):
    def get(self, request, *args, **kwargs):
        template_name = "EmergencyUser/DroneSend.html"
        return render(request, template_name, {'latitude' : kwargs['lat'], 'longitude' : kwargs ['lon']})
