from django.contrib import admin
from apps.incident.models import (
    Incident, IncidentType, InvolvedActor, IncidentImage
)


@admin.register(IncidentType)
class IncidentTypeAdmin(admin.ModelAdmin):
    list_display = ("name_bn", "name_en")
    search_fields = ("name_bn", "name_en")
    ordering = ("name_bn",)


@admin.register(InvolvedActor)
class InvolvedActorAdmin(admin.ModelAdmin):
    list_display = ("name_bn", "name_en")
    search_fields = ("name_bn", "name_en")
    ordering = ("name_bn",)


class IncidentImageInline(admin.TabularInline):
    model = IncidentImage
    extra = 1
    verbose_name = "ছবি"
    verbose_name_plural = "ছবিগুলো"


@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = (
        "title", "incident_type", "involved_actor",
        "division", "district", "date", "status"
    )
    list_filter = (
        "incident_type", "involved_actor", "division",
        "district", "status", "date"
    )
    search_fields = ("title", "description", "involved_actor__name_bn", "involved_actor__name_en")
    raw_id_fields = ("posted_by", "updated_by")
    inlines = [IncidentImageInline]
    date_hierarchy = "date"
    ordering = ("-date", "updated_at")


@admin.register(IncidentImage)
class IncidentImageAdmin(admin.ModelAdmin):
    list_display = ("incident", "image")
