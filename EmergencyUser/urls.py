from django.conf.urls import url, include

from django.http import HttpResponseRedirect
from .views.IndexViews import DroneDispatch, DroneSend, MissionStatusJSON, MissionStatusView
from django.urls import reverse

app_name = "EmergencyUser"
urlpatterns = [
    url(r'^DroneDispatch/$', DroneDispatch.as_view(), name='drone_dispatch'),
    url(r'^$', lambda r: HttpResponseRedirect(reverse('EmergencyUser:drone_dispatch')), name='index'),
    url(r'^DestinationSend/(?P<pk>\d+)/$', DroneSend.as_view(), name='destination_send'),
    url(r'^MissionStatusJSON/(?P<pk>\d+)/$', MissionStatusJSON.as_view(), name='mission_status_json'),
    url(r'^MissionStatus/(?P<pk>\d+)/$', MissionStatusView.as_view(), name='mission_status'),

]
