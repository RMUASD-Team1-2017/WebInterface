from django import forms
from geoposition import forms as geoforms

class DroneDestinationForm(forms.Form):
    destination = geoforms.GeopositionField()
