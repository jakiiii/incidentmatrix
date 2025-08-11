from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class IncidentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.incident'
    verbose_name = _("Incident")
