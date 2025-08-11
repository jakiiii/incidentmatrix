from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator

from apps.location.utils import district_image_directory_path


class District(models.Model):
    name_bn = models.CharField(
        max_length=30,
        verbose_name=_("জেলার নাম")
    )
    name_en = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        verbose_name=_("জেলার নাম (ইংরেজিতে)")
    )
    division = models.ForeignKey(
        'location.Division',
        on_delete=models.CASCADE,
        related_name='districts',
        verbose_name=_("বিভাগের নাম")
    )
    attachment = models.FileField(
        upload_to=district_image_directory_path,
        null=True,
        blank=True,
        verbose_name=_("জেলার ম্যাপ"),
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'svg'])]
    )

    def __str__(self):
        return self.name_bn

    class Meta:
        ordering = ('name_bn',)
        verbose_name = "District"
        verbose_name_plural = "District"
        db_table = "db_district"
