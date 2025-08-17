from django.db import models
from django.utils.translation import gettext_lazy as _

from django_countries.fields import CountryField


class InvolvedActor(models.Model):
    country = CountryField(
        blank_label="(select country)",
        null=True,
        blank=True,
        verbose_name=_('রাষ্ট্র/দেশ'),
    )
    name_bn = models.CharField(
        max_length=255,
        verbose_name=_("জড়িত ব্যক্তি/গোষ্ঠী/সংগঠন (বাংলা)"),
    )
    name_en = models.CharField(
        max_length=255,
        verbose_name=_("জড়িত ব্যক্তি/গোষ্ঠী/সংগঠন (ইংরেজি)"),
    )

    def __str__(self):
        return self.name_bn

    class Meta:
        ordering = ('name_bn',)
        verbose_name = "Involved Actor"
        verbose_name_plural = "Involved Actor"
        db_table = "db_involved_actor"
