from django.urls import path
from apps.incident.views import (
    IncidentListView, IncidentDetailView, IncidentMapView
)

app_name = "incident"


urlpatterns = [
    path('list/', IncidentListView.as_view(), name='incident_list'),
    path('detail/<int:pk>/', IncidentDetailView.as_view(), name='incident_detail'),
    path('list-maps/', IncidentMapView.as_view(), name='incident_list_maps'),
]
