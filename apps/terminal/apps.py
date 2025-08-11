from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TerminalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.terminal'
    verbose_name = _("Terminal")
