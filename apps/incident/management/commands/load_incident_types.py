from django.core.management.base import BaseCommand
from apps.incident.models import IncidentType

class Command(BaseCommand):
    help = 'Load predefined Incident Types into the database'

    def handle(self, *args, **kwargs):
        incident_types = [
            {"name_bn": "সীমান্ত হত্যাকাণ্ড", "name_en": "Border Killing"},
            {"name_bn": "অবৈধ সীমান্ত পারাপার", "name_en": "Illegal Border Crossing"},
            {"name_bn": "অবৈধ মানব পাচার", "name_en": "Illegal Human Trafficking"},
            {"name_bn": "পাহাড়ি সন্ত্রাসবাদ", "name_en": "Hill Tract Terrorism"},
            {"name_bn": "বন্যা", "name_en": "Flood"},
            {"name_bn": "ঘূর্ণিঝড়", "name_en": "Cyclone"},
            {"name_bn": "ভূমিধস", "name_en": "Landslide"},
            {"name_bn": "সংঘর্ষ", "name_en": "Clash"},
            {"name_bn": "অগ্নিকাণ্ড", "name_en": "Fire Incident"},
            {"name_bn": "সড়ক দুর্ঘটনা", "name_en": "Road Accident"},
            {"name_bn": "দাঙ্গা", "name_en": "Riot"},
            {"name_bn": "রাজনৈতিক সহিংসতা", "name_en": "Political Violence"},
            {"name_bn": "ধর্মীয় উত্তেজনা", "name_en": "Communal Tension"},
            {"name_bn": "অপহরণ", "name_en": "Abduction"},
            {"name_bn": "হত্যাকাণ্ড", "name_en": "Homicide"},
        ]

        for item in incident_types:
            obj, created = IncidentType.objects.get_or_create(
                name_bn=item["name_bn"],
                defaults={"name_en": item["name_en"]}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"✅ Created: {item['name_bn']}"))
            else:
                self.stdout.write(self.style.WARNING(f"⚠️ Already Exists: {item['name_bn']}"))
