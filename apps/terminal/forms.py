from django import forms
from django_countries.fields import Country
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
        # accept optional request if you pass it
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

        # ----- widgets / css -----
        self.fields["country"].widget.attrs.update({"class": "custom-select select2", "id": "id_country"})
        self.fields["state"].widget.attrs.update({"class": "custom-select select2", "id": "id_state"})
        self.fields["division"].widget.attrs.update({"class": "custom-select select2", "id": "id_division"})
        self.fields["district"].widget.attrs.update({"class": "custom-select select2", "id": "id_district"})
        self.fields["subdistrict"].widget.attrs.update({"class": "custom-select select2", "id": "id_subdistrict"})
        self.fields["incident_type"].widget.attrs.update({"class": "custom-select select2", "id": "incident_type"})
        self.fields["involved_actor"].widget.attrs.update({"class": "custom-select select2", "id": "involved_actor"})
        self.fields["title"].widget.attrs.update({"class": "form-control", "placeholder": "শিরনাম"})
        self.fields["latitude"].widget.attrs.update({"class": "form-control", "step": "any", "id": "id_latitude"})
        self.fields["longitude"].widget.attrs.update({"class": "form-control", "step": "any", "id": "id_longitude"})
        self.fields["date"].widget.attrs.update({"class": "form-control", "type": "datetime-local"})
        self.fields["description"].widget.attrs.update({"class": "form-control", "rows": 5, "id": "elm1"})

        # helpers
        def country_code_from_bound_or_instance():
            raw = self.data.get("country") if self.is_bound else (getattr(self.instance, "country", None) or self.initial.get("country"))
            code = getattr(raw, "code", raw) or ""
            return str(code).upper()

        def chosen(name):
            if self.is_bound:
                return self.data.get(name) or None
            return getattr(self.instance, name, None) or self.initial.get(name)

        code = country_code_from_bound_or_instance()
        division_id = chosen("division") or chosen("division_id")
        district_id = chosen("district") or chosen("district_id")

        # ----- location querysets -----
        self.fields["division"].queryset = Division.objects.order_by("name_bn")

        if division_id:
            qs_district = District.objects.filter(division_id=division_id).order_by("name_bn")
        elif getattr(self.instance, "division_id", None):
            qs_district = District.objects.filter(division_id=self.instance.division_id).order_by("name_bn")
        else:
            qs_district = District.objects.none()
        # include current selected district so it renders
        if getattr(self.instance, "district_id", None):
            qs_district = (District.objects.filter(pk=self.instance.district_id) | qs_district).distinct()
        self.fields["district"].queryset = qs_district

        if district_id:
            qs_sub = Subdistrict.objects.filter(district_id=district_id).order_by("name_bn")
        elif getattr(self.instance, "district_id", None):
            qs_sub = Subdistrict.objects.filter(district_id=self.instance.district_id).order_by("name_bn")
        else:
            qs_sub = Subdistrict.objects.none()
        # include current subdistrict
        if getattr(self.instance, "subdistrict_id", None):
            qs_sub = (Subdistrict.objects.filter(pk=self.instance.subdistrict_id) | qs_sub).distinct()
        self.fields["subdistrict"].queryset = qs_sub

        # ----- state by country (non-BD) -----
        if code and code != "BD":
            qs_state = State.objects.filter(country=code).order_by("name_bn")
            if getattr(self.instance, "state_id", None):
                qs_state = (State.objects.filter(pk=self.instance.state_id) | qs_state).distinct()
            self.fields["state"].queryset = qs_state
        else:
            self.fields["state"].queryset = State.objects.none()

        # ----- incident_type / involved_actor by country -----
        if code:
            qs_it = IncidentType.objects.filter(country=code).order_by("name_bn")
            if getattr(self.instance, "incident_type_id", None):
                # include current selected one even if its country is NULL/different
                qs_it = (IncidentType.objects.filter(pk=self.instance.incident_type_id) | qs_it).distinct()
            self.fields["incident_type"].queryset = qs_it

            qs_actor = InvolvedActor.objects.filter(country=code).order_by("name_bn")
            if getattr(self.instance, "involved_actor_id", None):
                qs_actor = (InvolvedActor.objects.filter(pk=self.instance.involved_actor_id) | qs_actor).distinct()
            self.fields["involved_actor"].queryset = qs_actor
        else:
            self.fields["incident_type"].queryset = IncidentType.objects.none()
            self.fields["involved_actor"].queryset = InvolvedActor.objects.none()

    # keep the BD vs non-BD validation here
    def clean(self):
        cleaned = super().clean()
        country = cleaned.get("country")
        state = cleaned.get("state")
        division = cleaned.get("division")
        district = cleaned.get("district")
        subdistrict = cleaned.get("subdistrict")

        code = (getattr(country, "code", country) or "").upper()

        if not code:
            self.add_error("country", "রাষ্ট্র/দেশ নির্বাচন করুন")
            return cleaned

        if code == "BD":
            if not division:
                self.add_error("division", "বিভাগ নির্বাচন করুন")
            if not district:
                self.add_error("district", "জেলা নির্বাচন করুন")
            if not subdistrict:
                self.add_error("subdistrict", "উপজেলা নির্বাচন করুন")
            if state:
                self.add_error("state", "বাংলাদেশের জন্য স্টেট/রাজ্য প্রযোজ্য নয়")
        else:
            if not state:
                self.add_error("state", "স্টেট/রাজ্য নির্বাচন করুন")
            if division:
                self.add_error("division", "অন্যান্য দেশের জন্য বিভাগ প্রযোজ্য নয়")
            if district:
                self.add_error("district", "অন্যান্য দেশের জন্য জেলা প্রযোজ্য নয়")
            if subdistrict:
                self.add_error("subdistrict", "অন্যান্য দেশের জন্য উপজেলা প্রযোজ্য নয়")

        return cleaned
