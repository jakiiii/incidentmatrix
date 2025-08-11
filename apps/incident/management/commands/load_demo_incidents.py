import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.incident.models import Incident, IncidentType, InvolvedActor
from apps.location.models import Division, District


class Command(BaseCommand):
    help = 'Load 20 demo incidents into the Incident model'

    def handle(self, *args, **kwargs):
        titles = [
            "বর্ডার এলাকায় গুলির ঘটনা", "মানব পাচারকারীদের আটক", "অভিযানে অস্ত্র উদ্ধার", "পাহাড়ি এলাকায় গোলাগুলি",
            "সড়ক দুর্ঘটনায় নিহত ৩", "বন্যায় শতাধিক ঘরবাড়ি বিধ্বস্ত", "অগ্নিকাণ্ডে ব্যাপক ক্ষয়ক্ষতি", "রাজনৈতিক মিছিলে সংঘর্ষ",
            "র‍্যাবের বিশেষ অভিযান", "অজ্ঞাত দুষ্কৃতিকারীর হামলা", "চোরাচালানের সময় ধৃত ব্যক্তি", "অপহরণের অভিযোগে মামলা",
            "ভূমিধসে বাড়িঘর ক্ষতিগ্রস্ত", "সাধারণ জনগণের প্রতিবাদ", "পরিবহন শ্রমিকদের ধর্মঘট", "ধর্মীয় উস্কানিমূলক বার্তা ভাইরাল",
            "স্থানীয় গোষ্ঠীর মধ্যে সংঘর্ষ", "সীমান্তে বিএসএফ-এর গুলি", "শিশু অপহরণের চেষ্টা ব্যর্থ", "নদী ভাঙনে গৃহহীন পরিবার"
        ]

        descriptions = [
            "আজ সকালে সীমান্তবর্তী এলাকায় গুলির ঘটনা ঘটে যেখানে একজন নিহত হয়।", "পুলিশ অভিযান চালিয়ে তিনজন মানব পাচারকারীকে আটক করেছে।",
            "র‍্যাবের অভিযানে একটি বাড়ি থেকে অস্ত্র উদ্ধার করা হয়।", "চট্টগ্রামের পাহাড়ি অঞ্চলে দুই গোষ্ঠীর মধ্যে সংঘর্ষ হয়।",
            "বাস ও ট্রাকের সংঘর্ষে তিনজন নিহত ও পাঁচজন আহত হয়েছে।", "বন্যায় ব্যাপক ক্ষয়ক্ষতি হয়েছে, বহু মানুষ গৃহহীন।",
            "বাজারে অগ্নিকাণ্ডে ২৫টি দোকান পুড়ে গেছে।", "মিছিলে দুই দলের মধ্যে ধাওয়া-পাল্টা ধাওয়ার ঘটনা ঘটে।",
            "বিশেষ অভিযানে বড় একটি সন্ত্রাসী চক্র ধরা পড়ে।", "দুর্বৃত্তরা হঠাৎ আক্রমণ চালায় এবং কয়েকজন আহত হয়।",
        ]

        incident_types = list(IncidentType.objects.all())
        actors = list(InvolvedActor.objects.all())
        divisions = list(Division.objects.all())
        status_choices = ['PUBLISHED']

        if not (incident_types and actors and divisions):
            self.stdout.write(self.style.ERROR("❌ Make sure IncidentType, InvolvedActor, and Division data exist."))
            return

        count = 0

        for i in range(20):
            title = random.choice(titles)
            description = random.choice(descriptions)
            incident_type = random.choice(incident_types)
            actor = random.choice(actors)
            division = random.choice(divisions)
            districts = list(division.districts.all())

            if not districts:
                continue  # Skip if division has no districts

            district = random.choice(districts)

            date = timezone.now() - timedelta(days=random.randint(1, 60))
            latitude = round(random.uniform(20.0, 26.5), 6)
            longitude = round(random.uniform(88.0, 92.5), 6)
            status = random.choice(status_choices)

            Incident.objects.create(
                title=title,
                description=description,
                incident_type=incident_type,
                involved_actor=actor,
                division=division,
                district=district,
                latitude=latitude,
                longitude=longitude,
                date=date,
                status=status
            )
            count += 1

        self.stdout.write(self.style.SUCCESS(f"✅ Successfully inserted {count} demo incidents."))
