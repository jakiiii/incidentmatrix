from django.contrib import admin
from apps.location.models import (
    District, Division, Subdistrict, State
)


@admin.register(Division)
class DivisionAdmin(admin.ModelAdmin):
    list_display = ['name_bn', 'name_en']


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ['name_bn', 'name_en', 'division']
    list_filter = ['division__name_bn', 'division__name_en']


@admin.register(Subdistrict)
class SubdistrictAdmin(admin.ModelAdmin):
    list_display = ['name_bn', 'name_en', 'district']
    list_filter = ['district__name_bn', 'district__division__name_bn']


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ['name_bn', 'name_en', 'country']
    list_filter = ['country']
