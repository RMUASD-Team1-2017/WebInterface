from django.conf.urls import url, include

from django.http import HttpResponseRedirect
from .views.IndexViews import Control
from django.urls import reverse

app_name = "EmergencyControl"
urlpatterns = [
    url(r'^control/$', Control.as_view(), name='control'),
    url(r'^$', lambda r: HttpResponseRedirect(reverse('EmergencyControl:control')), name='index')
]
