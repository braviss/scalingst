from django.http import JsonResponse
from location.models import Region, Locality

def get_regions(request, country_code):
    try:
        regions = Region.objects.filter(country=country_code)
        return JsonResponse({'regions': list(regions.values())})
    except Region.DoesNotExist:
        return JsonResponse({'error': 'Regions not found'}, status=404)

def get_localities(request, region_code):

    localities = Locality.objects.filter(region__code=region_code)
    return JsonResponse({'localities': list(localities.values())})
