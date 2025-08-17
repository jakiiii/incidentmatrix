from django.http import JsonResponse
from apps.location.models import (
    Division, District, Subdistrict, State
)


def get_states_by_country(request):
    code = (request.GET.get('country_code') or '').upper()
    rows = State.objects.filter(country=code).order_by('name_bn').values('id', 'name_bn')
    return JsonResponse(list(rows), safe=False)


def get_districts_by_division(request):
    division_id = request.GET.get('division_id')
    districts = District.objects.filter(division_id=division_id).values('id', 'name_bn')
    return JsonResponse(list(districts), safe=False)

def get_subdistricts_by_district(request):
    district_id = request.GET.get('district_id')
    subdistricts = Subdistrict.objects.filter(district_id=district_id).values('id', 'name_bn')
    return JsonResponse(list(subdistricts), safe=False)

def get_division_by_district(request, district_id):
    district = District.objects.filter(id=district_id).select_related('division').first()
    return JsonResponse({'division_id': district.division_id})

def get_parent_location_by_subdistrict(request, subdistrict_id):
    subdistrict = Subdistrict.objects.select_related('district__division').get(id=subdistrict_id)
    return JsonResponse({
        'district_id': subdistrict.district_id,
        'division_id': subdistrict.district.division_id
    })
