"""uasControlUI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include, static
from django.contrib import admin
from django.conf import settings
from EmergencyRabbitMQ import rabbit_sender, rabbit_receiver, rabbitCallbacks

urlpatterns = [
    url(r'^', include('EmergencyCommon.urls')),
    url(r'^EmergencyUser/', include('EmergencyUser.urls')),
    url(r'^EmergencyControl/', include('EmergencyControl.urls')),
    url(r'^$', lambda r: HttpResponseRedirect('EmergencyCommon/')),
    url(r'^admin/', admin.site.urls),

] + static.static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

#Hack... we start the rabbitmq consumer from here..

for x in rabbit_receiver: x.run()
rabbit_sender.run()
