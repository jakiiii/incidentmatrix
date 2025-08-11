from django.db import models
from django.utils.translation import gettext_lazy as _

from tinymce.models import HTMLField
from django_countries.fields import CountryField

from base.models import BaseModel


class Incident(BaseModel):
    country = CountryField(
        blank_label="(select country)",
        null=True,
        blank=True,
        verbose_name=_('রাষ্ট্র/দেশ'),
    )
    title = models.CharField(
        max_length=255,
        verbose_name=_("শিরনাম"),
    )
    description = HTMLField(
        blank=True,
        null=True,
        verbose_name=_("বিস্তারিত"),
    )
    incident_type = models.ForeignKey(
        'incident.IncidentType',
        on_delete=models.SET_NULL,
        null=True,
        related_name='incidents',
        verbose_name=_("ঘটনার ধরণ"),
    )
    involved_actor = models.ForeignKey(
        'incident.InvolvedActor',
        on_delete=models.SET_NULL,
        null=True,
        related_name='involved_actors',
        verbose_name=_("জড়িত ব্যক্তি/গোষ্ঠী/সংগঠন"),
    )
    division = models.ForeignKey(
        'location.Division',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='incident_divisions',
        verbose_name=_("বিভাগ"),
    )
    district = models.ForeignKey(
        'location.District',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='incident_districts',
        verbose_name=_("জেলা"),
    )
    subdistrict = models.ForeignKey(
        'location.Subdistrict',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='incident_subdistricts',
        verbose_name=_("উপজেলার নাম")
    )
    state = models.ForeignKey(
        'location.State',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='incident_states',
        verbose_name=_("স্টেট/রাজ্য")
    )
    latitude = models.FloatField(
        blank=True,
        null=True,
        verbose_name=_("অক্ষাংশ (ল্যাটিচুয়েড)"),
    )
    longitude = models.FloatField(
        blank=True,
        null=True,
        verbose_name=_("দ্রাঘিমাংশ (লংগিচুয়েড)"),
    )
    date = models.DateTimeField(
        verbose_name=_("ঘটনার তারিখ এবং সুময়"),
    )
    status = models.CharField(
        max_length=12,
        choices=BaseModel.StatusChoices.choices,
        default=BaseModel.StatusChoices.PUBLISHED,
        verbose_name=_("পাবলিশিং স্ট্যাটাস"),
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)
        verbose_name = "Incident"
        verbose_name_plural = "Incidents"
        db_table = "db_incidents"
