from django.urls import path
from apps.terminal.views import (
    TerminalView, IncidentCreateView, IncidentUpdateView, IncidentDeleteView
)

app_name = "terminal"


urlpatterns = [
    path('dashboard/', TerminalView.as_view(), name='terminal_dashboard'),
    path('incident-create/', IncidentCreateView.as_view(), name='incident_create'),
    path("incident/<int:pk>/edit/", IncidentUpdateView.as_view(), name="incident_update"),
    path("incident/<int:pk>/delete/", IncidentDeleteView.as_view(), name="incident_delete"),
]
