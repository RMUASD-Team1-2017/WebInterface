from django.shortcuts import render
from django.views.generic import View

class MainView(View):
    def get(self, request, *args, **kwargs):
        template_name = "EmergencyCommon/base.html"
        return render(request, template_name, {} )
