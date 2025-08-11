import json
import random
import calendar
from datetime import timedelta
from django.db.models import Count
from django.utils.timezone import now
from django.views.generic import TemplateView
from django.db.models.functions import TruncMonth

from core.mixins import AdministratorRequiredMixin

from apps.location.models import (
    Division, District
)

from apps.incident.models import (
    IncidentType, InvolvedActor, Incident, IncidentImage
)


def get_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)


class HomeView(AdministratorRequiredMixin, TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['title'] = 'Home'
        context['division_context'] = Division.objects.all().order_by('name_bn')
        context['district_context'] = District.objects.all().order_by('name_bn')
        context['incident_type_context'] = IncidentType.objects.all().order_by('name_bn')
        context['incident_actor_context'] = InvolvedActor.objects.all().order_by('name_bn')
        context['incident_of_bd'] = Incident.objects.filter(country='BD').count()
        context['incident_of_in'] = Incident.objects.filter(country='IN').count()
        context['incident_of_mm'] = Incident.objects.filter(country='MM').count()

        # Donut chart data with random color
        incident_type_data = (
            Incident.objects
            .values('incident_type__name_bn')
            .annotate(count=Count('id'))
            .order_by('-count')
        )

        chart_data = []
        chart_colors = []

        for item in incident_type_data:
            if item['incident_type__name_bn']:
                chart_data.append({
                    'label': item['incident_type__name_bn'],
                    'value': item['count']
                })
                chart_colors.append(get_random_color())

        context['donut_chart_data'] = chart_data
        context['donut_chart_colors'] = chart_colors

        # Line chart config
        today = now()
        last_year = today - timedelta(days=365)

        incidents = (
            Incident.objects.filter(date__gte=last_year)
            .annotate(month=TruncMonth('date'))
            .values('month', 'incident_type__name_bn')
            .annotate(total=Count('id'))
            .order_by('month')
        )

        # Prepare data for chart.js
        data_by_type = {}
        months_found = {entry['month'].strftime('%B') for entry in incidents}
        month_order = list(calendar.month_name)[1:]  # ['January', ..., 'December']
        all_months = [month for month in month_order if month in months_found]

        for entry in incidents:
            incident_type = entry['incident_type__name_bn']
            month = entry['month'].strftime('%B')
            count = entry['total']
            if incident_type not in data_by_type:
                data_by_type[incident_type] = {}
            data_by_type[incident_type][month] = count

        # Build dataset
        final_datasets = []
        color_palette = [
            '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF',
            '#FF9F40', '#00A6A6', '#FF6B6B', '#C9CBCF', '#845EC2',
            '#F67280', '#6C5B7B', '#355C7D', '#3EC1D3', '#FFD166'
        ]

        for idx, (incident_type, month_data) in enumerate(data_by_type.items()):
            dataset = {
                'label': incident_type,
                'data': [month_data.get(month, 0) for month in all_months],
                'fill': False,
                'borderColor': color_palette[idx % len(color_palette)],
                'tension': 0.3
            }
            final_datasets.append(dataset)

        context['chart_labels'] = json.dumps(all_months)
        context['chart_datasets'] = json.dumps(final_datasets)

        return context
