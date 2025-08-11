from django.conf import settings
from django.utils import timezone
from django.dispatch import Signal
from django.dispatch import receiver
from django.db.models.signals import post_save

from user_agents import parse
from ipware import get_client_ip
from geoip2.database import Reader

User = settings.AUTH_USER_MODEL
user_logged_in = Signal(['instance', 'request'])

from apps.accounts.models import UserLogs


@receiver(user_logged_in)
def log_user_login(sender, instance, request, **kwargs):
    user = instance  # 'instance' refers to the user who just logged in
    # ip_address = request.META.get('REMOTE_ADDR')
    ip_address, _ = get_client_ip(request)

    user_agent_string = request.META.get('HTTP_USER_AGENT')

    # Parse the user-agent string
    user_agent = parse(user_agent_string)

    # Extract browser, OS, and device info
    browser = f"{user_agent.browser.family} {user_agent.browser.version_string}"
    os = f"{user_agent.os.family} {user_agent.os.version_string}"
    device = user_agent.device.family

    # Activity log
    activity = f"User logged in from IP {ip_address} using {browser} on {os} with device {device}"

    # Fetch geo-location data using MaxMind GeoLite2
    location_data = {}
    try:
        reader = Reader(settings.GEOIP_PATH)
        response = reader.city(ip_address)
        location_data = {
            'city': response.city.name,
            'country': response.country.name,
            'latitude': response.location.latitude,
            'longitude': response.location.longitude,
        }
    except Exception as e:
        location_data = {
            'error': f"Failed to fetch location: {e}"
        }

    # Create a new log entry
    UserLogs.objects.create(
        user=user,
        activity=activity,
        ip_address=ip_address,
        device=device,  # Device info (e.g., mobile, desktop)
        os=os,  # Operating system
        user_agent=user_agent_string,
        location=location_data,
        action="Login"
    )
