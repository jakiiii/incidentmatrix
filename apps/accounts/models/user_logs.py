from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserLogs(models.Model):
    user = models.ForeignKey(
        'accounts.User',
        related_name='user_login_logs',
        on_delete=models.CASCADE,
        verbose_name=_("User")
    )
    activity = models.CharField(
        max_length=500,
        null=True,
        blank=True,
        verbose_name=_("Activity")
    )
    ip_address = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name=_("IP Address")
    )
    device = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Device")
    )
    os = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Operating System")
    )
    user_agent = models.TextField(
        null=True,
        blank=True,
        verbose_name=_("User Agent")
    )
    location = models.JSONField(
        null=True,
        blank=True,
        verbose_name=_("Location/GeoIP Data")
    )
    action = models.CharField(
        max_length=1000,
        null=True,
        blank=True,
        verbose_name=_("Action")
    )
    timestamp = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.ip_address} - {self.timestamp}"

    class Meta:
        verbose_name = "User Logs"
        verbose_name_plural = "User Logs"
        ordering = ('-timestamp',)
        db_table = "db_user_logs"
