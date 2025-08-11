from django.core.management.base import BaseCommand
from apps.location.models import Division

class Command(BaseCommand):
    help = 'Load all divisions of Bangladesh into the Division model'

    def handle(self, *args, **kwargs):
        divisions = [
            {"name_bn": "ঢাকা", "name_en": "Dhaka"},
            {"name_bn": "চট্টগ্রাম", "name_en": "Chattogram"},
            {"name_bn": "রাজশাহী", "name_en": "Rajshahi"},
            {"name_bn": "খুলনা", "name_en": "Khulna"},
            {"name_bn": "বরিশাল", "name_en": "Barisal"},
            {"name_bn": "সিলেট", "name_en": "Sylhet"},
            {"name_bn": "রংপুর", "name_en": "Rangpur"},
            {"name_bn": "ময়মনসিংহ", "name_en": "Mymensingh"},
        ]

        for item in divisions:
            obj, created = Division.objects.get_or_create(
                name_bn=item["name_bn"],
                defaults={"name_en": item["name_en"]}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"✅ Added: {item['name_bn']}"))
            else:
                self.stdout.write(self.style.WARNING(f"⚠️ Already exists: {item['name_bn']}"))
