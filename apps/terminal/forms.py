from django import forms
from apps.incident.models import Incident


class TerminalIncidentCreateForm(forms.ModelForm):

    class Meta:
        model = Incident
        fields = [
            "country", "state", "division", "district", "subdistrict",
            "title", "incident_type", "involved_actor",
            "latitude", "longitude", "date", "description",
        ]
