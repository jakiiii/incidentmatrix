from django.urls import path
from apps.location.views import (
    get_districts_by_division,
    get_subdistricts_by_district,
    get_division_by_district,
    get_parent_location_by_subdistrict
)

app_name = "location"


urlpatterns = [
    path('ajax/get-districts/', get_districts_by_division, name='get_districts_by_division'),
    path('ajax/subdistricts/', get_subdistricts_by_district, name='get_subdistricts_by_district'),
    path('ajax/district/<int:district_id>/division/', get_division_by_district, name='get_division_by_district'),
    path('ajax/subdistrict/<int:subdistrict_id>/parent/', get_parent_location_by_subdistrict, name='get_subdistrict_parent'),
]
