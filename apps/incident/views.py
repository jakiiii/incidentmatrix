import json
from datetime import datetime
from django.db.models import Q
from django.core import serializers
from django.http import JsonResponse
from django.utils.dateparse import parse_date, parse_time
from django.utils.safestring import mark_safe

from django_countries import countries

from django.views.generic  import (
    TemplateView, ListView, DetailView
)

from braces.views import LoginRequiredMixin

from apps.location.models import (
    Division, District, Subdistrict, State
)

from apps.incident.models import (
    IncidentType, InvolvedActor, Incident, IncidentImage
)


def parse_custom_date(date_str):
    try:
        return datetime.strptime(date_str, '%d/%m/%Y').date()
    except Exception:
        return None


class IncidentListView(LoginRequiredMixin, ListView):
    model = Incident
    context_object_name = 'incident_context'
    template_name = 'incident/incident_list.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().select_related(
            'state', 'division', 'district', 'subdistrict', 'incident_type', 'involved_actor'
        ).order_by('-date')

        # Get query parameters
        q = self.request.GET.get('q')
        country_code = self.request.GET.get('country_code')
        state_id = self.request.GET.get('state_id')
        division_id = self.request.GET.get('division_id')
        district_id = self.request.GET.get('district_id')
        subdistrict_id = self.request.GET.get('subdistrict_id')
        incident_type_id = self.request.GET.get('incident_type_id')
        involved_actor_id = self.request.GET.get('involved_actor_id')
        start_date = parse_custom_date(self.request.GET.get('start_date', ''))
        end_date = parse_custom_date(self.request.GET.get('end_date', ''))
        start_time = self.request.GET.get('start_time')
        end_time = self.request.GET.get('end_time')

        if q:
            queryset = queryset.filter(Q(title__icontains=q) | Q(description__icontains=q))

        if country_code:
            queryset = queryset.filter(country=country_code)

        if state_id:
            queryset = queryset.filter(state_id=state_id)

        if division_id:
            queryset = queryset.filter(division_id=division_id)

        if district_id:
            queryset = queryset.filter(district_id=district_id)

        if subdistrict_id:
            queryset = queryset.filter(subdistrict_id=subdistrict_id)

        if incident_type_id:
            queryset = queryset.filter(incident_type_id=incident_type_id)

        if involved_actor_id:
            queryset = queryset.filter(involved_actor_id=involved_actor_id)

        if start_date:
            queryset = queryset.filter(date__date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__date__lte=end_date)

        if start_time:
            queryset = queryset.filter(date__time__gte=parse_time(start_time))
        if end_time:
            queryset = queryset.filter(date__time__lte=parse_time(end_time))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home'
        context['state_context'] = State.objects.all().order_by('name_bn')
        context['division_context'] = Division.objects.all().order_by('name_bn')
        context['district_context'] = District.objects.all().order_by('name_bn')
        context['subdistrict_context'] = Subdistrict.objects.all().order_by('name_bn')
        context['incident_type_context'] = IncidentType.objects.all().order_by('name_bn')
        context['incident_actor_context'] = InvolvedActor.objects.all().order_by('name_bn')

        context['countries'] = [{'code': code, 'name': name} for code, name in countries]
        context['selected_country_code'] = self.request.GET.get('country_code', '')
        context['selected_state_id'] = self.request.GET.get('state_id', '')
        context['selected_division_id'] = self.request.GET.get('division_id', '')
        context['selected_district_id'] = self.request.GET.get('district_id', '')
        context['selected_subdistrict_id'] = self.request.GET.get('subdistrict_id', '')
        context['selected_incident_type_id'] = self.request.GET.get('incident_type_id', '')
        context['selected_involved_actor_id'] = self.request.GET.get('involved_actor_id', '')
        context['search_query'] = self.request.GET.get('q', '')
        context['start_date'] = self.request.GET.get('start_date', '')
        context['end_date'] = self.request.GET.get('end_date', '')
        context['start_time'] = self.request.GET.get('start_time', '')
        context['end_time'] = self.request.GET.get('end_time', '')
        return context


class IncidentDetailView(LoginRequiredMixin, DetailView):
    model = Incident
    template_name = 'incident/incident_detail.html'
    context_object_name = 'incident'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        return context


class IncidentMapView(LoginRequiredMixin, TemplateView):
    template_name = 'incident/incident_map.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request

        # GET parameters
        q = request.GET.get('q')
        country_code = request.GET.get('country_code')
        state_id = request.GET.get('id_state')
        division_id = request.GET.get('division_id')
        district_id = request.GET.get('district_id')
        subdistrict_id = request.GET.get('subdistrict_id')
        incident_type_id = request.GET.get('incident_type_id')
        involved_actor_id = request.GET.get('involved_actor_id')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        start_time = request.GET.get('start_time')
        end_time = request.GET.get('end_time')

        # Initial queryset
        incidents = Incident.objects.all()

        # Filtering
        if q:
            incidents = incidents.filter(Q(title__icontains=q) | Q(description__icontains=q))

        if country_code:
            incidents = incidents.filter(country=country_code)
        if state_id:
            incidents = incidents.filter(state_id=state_id)
        if division_id:
            incidents = incidents.filter(division_id=division_id)
        if district_id:
            incidents = incidents.filter(district_id=district_id)
        if subdistrict_id:
            incidents = incidents.filter(subdistrict_id=subdistrict_id)
        if incident_type_id:
            incidents = incidents.filter(incident_type_id=incident_type_id)
        if involved_actor_id:
            incidents = incidents.filter(involved_actor_id=involved_actor_id)

        # Date and time parsing (dd/mm/yyyy format)
        if start_date:
            try:
                start_datetime = datetime.strptime(start_date, '%d/%m/%Y')
                if start_time:
                    h, m = map(int, start_time.split(':'))
                    start_datetime = start_datetime.replace(hour=h, minute=m)
                incidents = incidents.filter(date__gte=start_datetime)
            except ValueError:
                pass

        if end_date:
            try:
                end_datetime = datetime.strptime(end_date, '%d/%m/%Y')
                if end_time:
                    h, m = map(int, end_time.split(':'))
                    end_datetime = end_datetime.replace(hour=h, minute=m)
                else:
                    end_datetime = end_datetime.replace(hour=23, minute=59, second=59)
                incidents = incidents.filter(date__lte=end_datetime)
            except ValueError:
                pass

        # Exclude incidents with null lat/lng
        incidents = incidents.exclude(latitude__isnull=True, longitude__isnull=True)

        # Prepare JSON
        incident_data = [{
            'id': i.id,
            'title': i.title,
            'lat': i.latitude,
            'lng': i.longitude,
            'description': i.description,
            'date': i.date.strftime('%Y-%m-%d %H:%M'),
        } for i in incidents]

        # Context
        context['incident_json'] = mark_safe(json.dumps(incident_data))
        context['selected_country_code'] = country_code or ''
        context['selected_state_id'] = state_id or ''
        context['selected_division_id'] = division_id or ''
        context['selected_district_id'] = district_id or ''
        context['selected_subdistrict_id'] = subdistrict_id or ''
        context['selected_incident_type_id'] = incident_type_id or ''
        context['selected_involved_actor_id'] = involved_actor_id or ''
        context['start_date'] = start_date or ''
        context['end_date'] = end_date or ''
        context['start_time'] = start_time or ''
        context['end_time'] = end_time or ''

        context['countries'] = [{'code': code, 'name': name} for code, name in countries]
        context['state_context'] = State.objects.all().order_by('name_bn')
        context['division_context'] = Division.objects.all().order_by('name_bn')
        context['district_context'] = District.objects.all().order_by('name_bn')
        context['subdistrict_context'] = Subdistrict.objects.all().order_by('name_bn')
        context['incident_type_context'] = IncidentType.objects.all().order_by('name_bn')
        context['incident_actor_context'] = InvolvedActor.objects.all().order_by('name_bn')
        return context
