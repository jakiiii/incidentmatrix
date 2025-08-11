from django.db import models
from django.utils.translation import gettext_lazy as _


class Subdistrict(models.Model):
    name_bn = models.CharField(
        max_length=30,
        verbose_name=_("উপজেলার নাম")
    )
    name_en = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        verbose_name=_("উপজেলার নাম (ইংরেজিতে)")
    )
    district = models.ForeignKey(
        'location.District',
        on_delete=models.CASCADE,
        related_name='subdistricts',
        verbose_name=_("জেলার নাম")
    )

    def __str__(self):
        return self.name_bn

    class Meta:
        ordering = ('name_bn',)
        verbose_name = "Sub-District"
        verbose_name_plural = "Sub-District"
        db_table = "db_subdistrict"
