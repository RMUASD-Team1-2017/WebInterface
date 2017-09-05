from django.conf.urls import url, include

from django.http import HttpResponseRedirect
from .views.IndexViews import MainView

app_name = "EmergencyCommon"
urlpatterns = [
    url(r'^$', MainView.as_view(), name='index'),

]
