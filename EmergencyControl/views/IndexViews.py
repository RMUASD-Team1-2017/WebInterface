from django.shortcuts import render
from django.views.generic import View

class Control(View):
    def get(self, request, *args, **kwargs):
        template_name = "EmergencyControl/controlIndex.html"
        return render(request, template_name, {} )
