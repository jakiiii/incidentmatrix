from django import forms

from apps.incident.models import Incident, IncidentType, InvolvedActor
from apps.location.models import State, Division, District, Subdistrict


class TerminalIncidentCreateForm(forms.ModelForm):
    class Meta:
        model = Incident
        fields = [
            "country", "state", "division", "district", "subdistrict",
            "title", "incident_type", "involved_actor",
            "latitude", "longitude", "date", "description",
        ]

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

        # ---- Widgets / IDs for JS / Select2 ----
        self.fields["country"].widget.attrs.update({"class": "custom-select select2", "id": "id_country"})
        self.fields["state"].widget.attrs.update({"class": "custom-select select2", "id": "id_state"})
        self.fields["division"].widget.attrs.update({"class": "custom-select select2", "id": "id_division"})
        self.fields["district"].widget.attrs.update({"class": "custom-select select2", "id": "id_district"})
        self.fields["subdistrict"].widget.attrs.update({"class": "custom-select select2", "id": "id_subdistrict"})
        self.fields["title"].widget.attrs.update({"class": "form-control", "placeholder": "শিরনাম"})
        self.fields["incident_type"].widget.attrs.update({"class": "custom-select select2"})
        self.fields["involved_actor"].widget.attrs.update({"class": "custom-select select2"})
        self.fields["latitude"].widget.attrs.update({"class": "form-control", "step": "any", "id": "id_latitude"})
        self.fields["longitude"].widget.attrs.update({"class": "form-control", "step": "any", "id": "id_longitude"})
        self.fields["date"].widget.attrs.update({"class": "form-control", "type": "datetime-local"})
        self.fields["description"].widget.attrs.update({"class": "form-control", "rows": 5, "id": "elm1"})

        # ---- Base querysets ----
        self.fields["state"].queryset = State.objects.order_by("name_bn")
        self.fields["division"].queryset = Division.objects.order_by("name_bn")
        self.fields["district"].queryset = District.objects.order_by("name_bn")
        self.fields["subdistrict"].queryset = Subdistrict.objects.order_by("name_bn")

        # ---- Narrow by user selections (if request present) ----
        if request:
            data = request.POST or request.GET
            country_raw = data.get('country')
            country_code = getattr(country_raw, 'code', country_raw) or ''
            country_code = str(country_code).upper()

            division_id = data.get("division") or data.get("division_id")
            district_id = data.get("district") or data.get("district_id")

            # State list depends on non-BD countries
            if country_code and country_code != 'BD':
                self.fields['state'].queryset = State.objects.filter(country=country_code).order_by('name_bn')
            elif country_code == 'BD':
                self.fields['state'].queryset = State.objects.none()

            # IncidentType / InvolvedActor by country
            if country_code:
                self.fields['incident_type'].queryset = IncidentType.objects.filter(
                    country=country_code
                ).order_by('name_bn')
                self.fields['involved_actor'].queryset = InvolvedActor.objects.filter(
                    country=country_code
                ).order_by('name_bn')

            # Division → District → Subdistrict narrowing
            if division_id:
                self.fields["district"].queryset = District.objects.filter(
                    division_id=division_id
                ).order_by("name_bn")

            if district_id:
                self.fields["subdistrict"].queryset = Subdistrict.objects.filter(
                    district_id=district_id
                ).order_by("name_bn")

    # ---- Business rules moved here ----
    def clean(self):
        cleaned = super().clean()

        country = cleaned.get("country")
        state = cleaned.get("state")
        division = cleaned.get("division")
        district = cleaned.get("district")
        subdistrict = cleaned.get("subdistrict")

        # country may be a Country object OR a string like "BD"
        country_code = getattr(country, "code", country) or ""
        country_code = str(country_code).upper()

        if not country_code:
            self.add_error("country", "রাষ্ট্র/দেশ নির্বাচন করুন")
            return cleaned

        if country_code == "BD":
            # Require BD chain; forbid state
            if not division:
                self.add_error("division", "বিভাগ নির্বাচন করুন")
            if not district:
                self.add_error("district", "জেলা নির্বাচন করুন")
            if not subdistrict:
                self.add_error("subdistrict", "উপজেলা নির্বাচন করুন")
            if state:
                self.add_error("state", "বাংলাদেশের জন্য স্টেট/রাজ্য প্রযোজ্য নয়")
        else:
            # Require state; forbid BD chain
            if not state:
                self.add_error("state", "স্টেট/রাজ্য নির্বাচন করুন")
            if division:
                self.add_error("division", "অন্যান্য দেশের জন্য বিভাগ প্রযোজ্য নয়")
            if district:
                self.add_error("district", "অন্যান্য দেশের জন্য জেলা প্রযোজ্য নয়")
            if subdistrict:
                self.add_error("subdistrict", "অন্যান্য দেশের জন্য উপজেলা প্রযোজ্য নয়")

        return cleaned
