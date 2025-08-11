from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator

from apps.incident.utils import incident_image_directory_path


class IncidentImage(models.Model):
    incident = models.ForeignKey(
        'incident.Incident',
        on_delete=models.CASCADE,
        related_name='incident_images',
        verbose_name=_("ইন্সিডেন্ট"),
    )
    image = models.FileField(
        upload_to=incident_image_directory_path,
        null=True,
        blank=True,
        verbose_name=_("ছবি"),
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'svg'])]
    )

    class Meta:
        verbose_name = "Incident Image"
        verbose_name_plural = "Incident Images"
        db_table = "db_incident_images"
