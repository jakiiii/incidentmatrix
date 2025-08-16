from django.views.generic import TemplateView, ListView, CreateView

from django.contrib import messages
from django.urls import reverse_lazy

from apps.terminal.forms import TerminalIncidentCreateForm
from apps.incident.models import Incident
from apps.location.models import Division, District, Subdistrict, State

from core.mixins import OperatorRequiredMixin


class TerminalView(OperatorRequiredMixin, ListView):
    model = Incident
    template_name = 'terminal/terminal.html'
    context_object_name = 'incident_context'
    paginate_by = 10

    def get_queryset(self):
        return Incident.objects.filter(posted_by=self.request.user).order_by('-updated_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.request.user.get_full_name()
        return context


class IncidentCreateView(OperatorRequiredMixin, CreateView):
    model = Incident
    form_class = TerminalIncidentCreateForm
    template_name = "terminal/incident_create.html"
    success_url = reverse_lazy("terminal:terminal_dashboard")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["title"] = "নতুন ইন্সিডেন্ট যুক্ত করুন"
        return ctx

    def get_form(self, form_class=None):
        """
        Keep ALL display logic, queryset narrowing, and widget setup here.
        The form class stays thin.
        """
        form = super().get_form(form_class)

        # ----- Widgets / classes / ids for JS -----
        form.fields["country"].widget.attrs.update({"class": "custom-select select2", "id": "id_country"})
        form.fields["state"].widget.attrs.update({"class": "custom-select select2", "id": "id_state"})
        form.fields["division"].widget.attrs.update({"class": "custom-select select2", "id": "id_division"})
        form.fields["district"].widget.attrs.update({"class": "custom-select select2", "id": "id_district"})
        form.fields["subdistrict"].widget.attrs.update({"class": "custom-select select2", "id": "id_subdistrict"})
        form.fields["title"].widget.attrs.update({"class": "form-control", "placeholder": "শিরনাম"})
        form.fields["incident_type"].widget.attrs.update({"class": "custom-select select2"})
        form.fields["involved_actor"].widget.attrs.update({"class": "custom-select select2"})
        form.fields["latitude"].widget.attrs.update({"class": "form-control", "step": "any"})
        form.fields["longitude"].widget.attrs.update({"class": "form-control", "step": "any"})
        form.fields["date"].widget.attrs.update({"class": "form-control", "type": "datetime-local"})
        form.fields["description"].widget.attrs.update({"class": "form-control", "rows": 5, "id": "elm1"})

        # ----- Default querysets -----
        form.fields["state"].queryset = State.objects.order_by("name_bn")
        form.fields["division"].queryset = Division.objects.order_by("name_bn")
        form.fields["district"].queryset = District.objects.order_by("name_bn")
        form.fields["subdistrict"].queryset = Subdistrict.objects.order_by("name_bn")

        # ----- Narrow children by user selections (POST first, then GET) -----
        data = self.request.POST or self.request.GET
        division_id = data.get("division") or data.get("division_id")
        district_id = data.get("district") or data.get("district_id")

        if division_id:
            form.fields["district"].queryset = District.objects.filter(
                division_id=division_id
            ).order_by("name_bn")

        if district_id:
            form.fields["subdistrict"].queryset = Subdistrict.objects.filter(
                district_id=district_id
            ).order_by("name_bn")

        return form

    # ---- Keep business rules in the view ----
    def _apply_business_rules(self, form) -> bool:
        """
        Rules:
        - If country == BD → require division/district/subdistrict; forbid state.
        - Else (non-BD) → require state; forbid division/district/subdistrict.
        """
        cleaned = form.cleaned_data
        country = cleaned.get("country")
        state = cleaned.get("state")
        division = cleaned.get("division")
        district = cleaned.get("district")
        subdistrict = cleaned.get("subdistrict")

        # country may be a Country object OR a simple string like "BD"
        country_code = getattr(country, "code", country) or ""  # normalize to string
        country_code = str(country_code).upper()

        ok = True
        if not country_code:
            form.add_error("country", "রাষ্ট্র/দেশ নির্বাচন করুন")
            return False

        if country_code == "BD":
            if not division:
                form.add_error("division", "বিভাগ নির্বাচন করুন");
                ok = False
            if not district:
                form.add_error("district", "জেলা নির্বাচন করুন");
                ok = False
            if not subdistrict:
                form.add_error("subdistrict", "উপজেলা নির্বাচন করুন");
                ok = False
            if state:
                form.add_error("state", "বাংলাদেশের জন্য স্টেট/রাজ্য প্রযোজ্য নয়");
                ok = False
        else:
            if not state:
                form.add_error("state", "স্টেট/রাজ্য নির্বাচন করুন");
                ok = False
            if division:
                form.add_error("division", "অন্যান্য দেশের জন্য বিভাগ প্রযোজ্য নয়");
                ok = False
            if district:
                form.add_error("district", "অন্যান্য দেশের জন্য জেলা প্রযোজ্য নয়");
                ok = False
            if subdistrict:
                form.add_error("subdistrict", "অন্যান্য দেশের জন্য উপজেলা প্রযোজ্য নয়");
                ok = False

        return ok

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid() and self._apply_business_rules(form):
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        obj = form.save(commit=False)
        if hasattr(obj, "posted_by_id"):
            obj.posted_by = self.request.user
        obj.save()
        messages.success(self.request, "ইন্সিডেন্ট সফলভাবে যুক্ত হয়েছে।")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "ফর্মে ত্রুটি আছে, অনুগ্রহ করে ঠিক করুন।")
        return super().form_invalid(form)
