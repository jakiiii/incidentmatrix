from django.db import models
from django.utils.translation import gettext_lazy as _


class IncidentType(models.Model):
    name_bn = models.CharField(
        max_length=100,
        verbose_name=_("ঘটনার ধরণ (বাংলা)"),
    )
    name_en = models.CharField(
        max_length=100,
        verbose_name=_("ঘটনার ধরণ (ইংরেজি)"),
    )

    def __str__(self):
        return self.name_bn

    class Meta:
        ordering = ('name_bn',)
        verbose_name = "Incident Type"
        verbose_name_plural = "Incident Type"
        db_table = "db_incident_type"
