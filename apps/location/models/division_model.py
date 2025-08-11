from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator

from apps.location.utils import division_image_directory_path


class Division(models.Model):
    name_bn = models.CharField(
        max_length=25,
        verbose_name=_('বিভাগের নাম')
    )
    name_en = models.CharField(
        max_length=25,
        null=True,
        blank=True,
        verbose_name=_('বিভাগের নাম (ইংরেজিতে)')
    )
    attachment = models.FileField(
        upload_to=division_image_directory_path,
        null=True,
        blank=True,
        verbose_name=_("বিভাগের ম্যাপ"),
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'svg'])]
    )

    def __str__(self):
        return self.name_bn

    class Meta:
        ordering = ('name_bn',)
        verbose_name = "Division"
        verbose_name_plural = "Division"
        db_table = "db_division"
