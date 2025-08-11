from django.core.management.base import BaseCommand
from apps.location.models import Subdistrict, District

# Sample data structure — fill it with all 395 subdistricts
SUBDISTRICT_DATA = [
    # Format: ("Subdistrict Name BN", "Subdistrict Name EN", "District Name EN")
    ("সদর", "Sadar", "Dhaka"),
    ("সাভার", "Savar", "Dhaka"),
    ("দোহার", "Dohar", "Dhaka"),
    ("কেরানীগঞ্জ", "Keraniganj", "Dhaka"),
    ("নওগাঁ সদর", "Naogaon Sadar", "Naogaon"),
    # ... Add the remaining 390+ entries
]

class Command(BaseCommand):
    help = 'Load Subdistricts into the database'

    def handle(self, *args, **kwargs):
        created_count = 0
        for name_bn, name_en, district_name_en in SUBDISTRICT_DATA:
            try:
                district = District.objects.get(name_en__iexact=district_name_en)
                obj, created = Subdistrict.objects.get_or_create(
                    name_bn=name_bn,
                    name_en=name_en,
                    district=district
                )
                if created:
                    created_count += 1
            except District.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"District '{district_name_en}' not found. Skipping '{name_bn}'"))

        self.stdout.write(self.style.SUCCESS(f"Subdistrict import complete. {created_count} new entries added."))
