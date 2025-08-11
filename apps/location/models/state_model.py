from django.db import models
from django.utils.translation import gettext_lazy as _

from django_countries.fields import CountryField


class State(models.Model):
    name_bn = models.CharField(
        max_length=30,
        verbose_name=_("স্টেট/রাজ্য নাম")
    )
    name_en = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        verbose_name=_("স্টেট নাম (ইংরেজিতে)")
    )
    country = CountryField(
        blank_label="(select country)",
        verbose_name=_('রাষ্ট্র/দেশ'),
    )

    def __str__(self):
        return self.name_bn

    class Meta:
        ordering = ('name_bn',)
        verbose_name = "State"
        verbose_name_plural = "State"
        db_table = "db_states"
