from django.core.management.base import BaseCommand
from apps.incident.models import InvolvedActor

class Command(BaseCommand):
    help = 'Load demo Involved Actors into the database'

    def handle(self, *args, **kwargs):
        actors = [
            {"name_bn": "বিজিবি", "name_en": "BGB (Border Guard Bangladesh)"},
            {"name_bn": "বিএসএফ", "name_en": "BSF (Border Security Force, India)"},
            {"name_bn": "র‍্যাব", "name_en": "RAB (Rapid Action Battalion)"},
            {"name_bn": "পুলিশ", "name_en": "Police"},
            {"name_bn": "সন্ত্রাসী গোষ্ঠী", "name_en": "Terrorist Group"},
            {"name_bn": "পাহাড়ি বিচ্ছিন্নতাবাদী", "name_en": "Hill Separatist Group"},
            {"name_bn": "মানব পাচারকারী চক্র", "name_en": "Human Trafficking Ring"},
            {"name_bn": "অজ্ঞাতনামা ব্যক্তি", "name_en": "Unknown Individual"},
            {"name_bn": "ছাত্র সংগঠন", "name_en": "Student Group"},
            {"name_bn": "রাজনৈতিক সংগঠন", "name_en": "Political Group"},
            {"name_bn": "সাধারণ জনগণ", "name_en": "Civilians"},
            {"name_bn": "স্থানীয় গোষ্ঠী", "name_en": "Local Group"},
            {"name_bn": "পরিবহন শ্রমিক", "name_en": "Transport Workers"},
            {"name_bn": "দুর্বৃত্ত দল", "name_en": "Miscreant Group"},
        ]

        for item in actors:
            obj, created = InvolvedActor.objects.get_or_create(
                name_bn=item["name_bn"],
                defaults={"name_en": item["name_en"]}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"✅ Created: {item['name_bn']}"))
            else:
                self.stdout.write(self.style.WARNING(f"⚠️ Already exists: {item['name_bn']}"))
