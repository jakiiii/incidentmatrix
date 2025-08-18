from django.conf import settings
from django.views.generic import TemplateView, ListView, CreateView, UpdateView

from django.contrib import messages
from django.urls import reverse_lazy

from apps.terminal.forms import TerminalIncidentCreateForm
from apps.incident.models import Incident, IncidentType, InvolvedActor, IncidentImage
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
        ctx['map_key'] = settings.GOOGLE_MAP_KEY
        return ctx

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request  # pass request into the form
        return kwargs

    def form_valid(self, form):
        obj = form.save(commit=False)
        if hasattr(obj, "posted_by_id"):
            obj.posted_by = self.request.user
        obj.save()

        # Save images (multiple)
        files = self.request.FILES.getlist("images")
        for f in files:
            # (validators on IncidentImage will enforce extensions)
            IncidentImage.objects.create(incident=obj, image=f)

        messages.success(self.request, "ইন্সিডেন্ট সফলভাবে যুক্ত হয়েছে এবং ছবিগুলো সংরক্ষিত হয়েছে।")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "ফর্মে ত্রুটি আছে, অনুগ্রহ করে ঠিক করুন।")
        return super().form_invalid(form)
