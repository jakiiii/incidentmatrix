from django.urls import path
from apps.terminal.views import (
    TerminalView, IncidentCreateView
)

app_name = "terminal"


urlpatterns = [
    path('dashboard/', TerminalView.as_view(), name='terminal_dashboard'),
    path('incident-create/', IncidentCreateView.as_view(), name='incident_create'),
]
