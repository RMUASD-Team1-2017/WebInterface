from django.shortcuts import render
from django.views.generic import View
from EmergencyCommon.models import DroneMission
from django.http import HttpResponseRedirect, Http404, JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from EmergencyRabbitMQ import rabbitSenders
import json
class Control(View):
    def get(self, request, *args, **kwargs):
        template_name = "EmergencyControl/controlIndex.html"
        return render(request, template_name, {} )
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            try:
                data = json.loads(request.body)
            except:
                return HttpResponse(status=400) #Bad request
            try:
                decision = data["decision"]
                mission = get_object_or_404(DroneMission, pk = int(data["mission"]))
            except (KeyError, ValueError):
                return HttpResponse(status=400) #Bad request
            if not decision in ["accept", "deny"]:
                return HttpResponse(status=400) #Bad request
        else:
            return HttpResponse(status=400) #Bad request

        #Send request for mission
        if decision == "accept":
            rabbitSenders.send_mission_request(mission = mission)
            mission.accepted = True
        else:
            mission.accepted = False
        mission.save()

        return HttpResponse(status=204)

class MissionListJSON(View):
    def get(self, request, *args, **kwargs):
        template_name = "EmergencyControl/controlIndex.html"
        accepted_str = kwargs["accepted"]
        if accepted_str == "True":
            accepted = True
        elif accepted_str == "False":
            accepted = False
        else:
            accepted = None
        missions = DroneMission.objects.filter(accepted = accepted)
        response = {}
        for mission in list(missions):
            response[mission.id] = {}
            response[mission.id]['last_update'] = mission.last_update
            response[mission.id]['accepted'] = mission.accepted
            response[mission.id]['goal'] = {'latitude' : mission.goal_latitude, 'longtitude' : mission.goal_longtitude}
            response[mission.id]['waypoint'] = {'latitude' : mission.waypoint_latitude, 'longtitude' : mission.waypoint_longtitude}
            response[mission.id]['call_position'] = {'latitude' : mission.call_latitude, 'longtitude' : mission.call_longtitude}
            response[mission.id]['position'] = {'latitude' : None, 'longtitude' : None}
            response[mission.id]['eta'] = mission.eta
            response[mission.id]['takeoff_done'] = False
            response[mission.id]['state'] = None
            if mission.the_drone:
                response[mission.id]['position']['latitude'] = mission.the_drone.latitude
                response[mission.id]['position']['longtitude'] = mission.the_drone.longtitude
                response[mission.id]['takeoff_done'] = True
                response[mission.id]['state'] = mission.the_drone.state

        return JsonResponse(response)
