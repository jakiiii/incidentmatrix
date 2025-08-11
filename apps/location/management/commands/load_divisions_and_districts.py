from django.core.management.base import BaseCommand
from apps.location.models import Division, District

class Command(BaseCommand):
    help = 'Load all Bangladesh divisions and their districts'

    def handle(self, *args, **kwargs):
        divisions_and_districts = {
            "Dhaka": {
                "bn": "ঢাকা",
                "districts": [
                    ("ঢাকা", "Dhaka"),
                    ("গাজীপুর", "Gazipur"),
                    ("নারায়ণগঞ্জ", "Narayanganj"),
                    ("টাঙ্গাইল", "Tangail"),
                    ("কিশোরগঞ্জ", "Kishoreganj"),
                    ("মানিকগঞ্জ", "Manikganj"),
                    ("নরসিংদী", "Narsingdi"),
                    ("মুন্সিগঞ্জ", "Munshiganj"),
                    ("রাজবাড়ী", "Rajbari"),
                    ("ফরিদপুর", "Faridpur"),
                    ("গোপালগঞ্জ", "Gopalganj"),
                    ("মাদারীপুর", "Madaripur"),
                    ("শরীয়তপুর", "Shariatpur"),
                ]
            },
            "Chattogram": {
                "bn": "চট্টগ্রাম",
                "districts": [
                    ("চট্টগ্রাম", "Chattogram"),
                    ("কক্সবাজার", "Cox's Bazar"),
                    ("বান্দরবান", "Bandarban"),
                    ("খাগড়াছড়ি", "Khagrachhari"),
                    ("রাঙ্গামাটি", "Rangamati"),
                    ("নোয়াখালী", "Noakhali"),
                    ("লক্ষ্মীপুর", "Laxmipur"),
                    ("ফেনী", "Feni"),
                    ("চাঁদপুর", "Chandpur"),
                    ("কুমিল্লা", "Cumilla"),
                    ("ব্রাহ্মণবাড়িয়া", "Brahmanbaria"),
                ]
            },
            "Rajshahi": {
                "bn": "রাজশাহী",
                "districts": [
                    ("রাজশাহী", "Rajshahi"),
                    ("চাঁপাইনবাবগঞ্জ", "Chapainawabganj"),
                    ("নওগাঁ", "Naogaon"),
                    ("নাটোর", "Natore"),
                    ("পাবনা", "Pabna"),
                    ("বগুড়া", "Bogra"),
                    ("জয়পুরহাট", "Joypurhat"),
                    ("সিরাজগঞ্জ", "Sirajganj"),
                ]
            },
            "Khulna": {
                "bn": "খুলনা",
                "districts": [
                    ("খুলনা", "Khulna"),
                    ("বাগেরহাট", "Bagerhat"),
                    ("সাতক্ষীরা", "Satkhira"),
                    ("যশোর", "Jashore"),
                    ("নড়াইল", "Narail"),
                    ("মাগুরা", "Magura"),
                    ("ঝিনাইদহ", "Jhenaidah"),
                    ("চুয়াডাঙ্গা", "Chuadanga"),
                    ("কুষ্টিয়া", "Kushtia"),
                    ("মেহেরপুর", "Meherpur"),
                ]
            },
            "Barisal": {
                "bn": "বরিশাল",
                "districts": [
                    ("বরিশাল", "Barisal"),
                    ("পটুয়াখালী", "Patuakhali"),
                    ("ভোলা", "Bhola"),
                    ("পিরোজপুর", "Pirojpur"),
                    ("ঝালকাঠি", "Jhalokathi"),
                    ("বরগুনা", "Barguna"),
                ]
            },
            "Sylhet": {
                "bn": "সিলেট",
                "districts": [
                    ("সিলেট", "Sylhet"),
                    ("সুনামগঞ্জ", "Sunamganj"),
                    ("মৌলভীবাজার", "Moulvibazar"),
                    ("হবিগঞ্জ", "Habiganj"),
                ]
            },
            "Rangpur": {
                "bn": "রংপুর",
                "districts": [
                    ("রংপুর", "Rangpur"),
                    ("দিনাজপুর", "Dinajpur"),
                    ("গাইবান্ধা", "Gaibandha"),
                    ("কুড়িগ্রাম", "Kurigram"),
                    ("লালমনিরহাট", "Lalmonirhat"),
                    ("নীলফামারী", "Nilphamari"),
                    ("ঠাকুরগাঁও", "Thakurgaon"),
                    ("পঞ্চগড়", "Panchagarh"),
                ]
            },
            "Mymensingh": {
                "bn": "ময়মনসিংহ",
                "districts": [
                    ("ময়মনসিংহ", "Mymensingh"),
                    ("জামালপুর", "Jamalpur"),
                    ("নেত্রকোণা", "Netrokona"),
                    ("শেরপুর", "Sherpur"),
                ]
            },
        }

        for div_en, data in divisions_and_districts.items():
            div_bn = data["bn"]
            division, created = Division.objects.get_or_create(name_en=div_en, defaults={"name_bn": div_bn})
            if created:
                self.stdout.write(self.style.SUCCESS(f"✅ Division added: {div_bn} ({div_en})"))
            else:
                self.stdout.write(self.style.WARNING(f"⚠️ Division exists: {div_bn}"))

            for dist_bn, dist_en in data["districts"]:
                district, created = District.objects.get_or_create(
                    name_bn=dist_bn,
                    name_en=dist_en,
                    division=division
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"   ➕ District added: {dist_bn} ({dist_en})"))
                else:
                    self.stdout.write(self.style.WARNING(f"   ⚠️ District exists: {dist_bn}"))
