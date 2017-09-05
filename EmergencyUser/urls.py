from django.conf.urls import url, include

from django.http import HttpResponseRedirect
from .views.IndexViews import DroneDispatch, DroneSend
from django.urls import reverse

app_name = "EmergencyUser"
urlpatterns = [
    url(r'^DroneDispatch/$', DroneDispatch.as_view(), name='drone_dispatch'),
    url(r'^$', lambda r: HttpResponseRedirect(reverse('EmergencyUser:drone_dispatch')), name='index'),
    #Regular expression for latitude and longtitude: https://stackoverflow.com/questions/3518504/regular-expression-for-matching-latitude-longitude-coordinates
    #Fetches DestionSend/lat_lon
    url(r'^DestinationSend/(?P<lat>(\+|-)?(?:90(?:(?:\.0{1,30})?)|(?:[0-9]|[1-8][0-9])(?:(?:\.[0-9]{1,30})?)))_(?P<lon>(\+|-)?(?:180(?:(?:\.0{1,30})?)|(?:[0-9]|[1-9][0-9]|1[0-7][0-9])(?:(?:\.[0-9]{1,30})?)))/$', DroneSend.as_view(), name='destination_send'),

]
