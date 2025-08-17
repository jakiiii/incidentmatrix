from django.urls import path
from apps.incident.views import (
    IncidentListView, IncidentDetailView, IncidentMapView,
    get_incident_types_by_country, get_involved_actors_by_country
)

app_name = "incident"


urlpatterns = [
    path('ajax/incident-types/', get_incident_types_by_country, name='get_incident_types_by_country'),
    path('ajax/involved-actors/', get_involved_actors_by_country, name='get_involved_actors_by_country'),
    path('list/', IncidentListView.as_view(), name='incident_list'),
    path('detail/<int:pk>/', IncidentDetailView.as_view(), name='incident_detail'),
    path('list-maps/', IncidentMapView.as_view(), name='incident_list_maps'),
]
