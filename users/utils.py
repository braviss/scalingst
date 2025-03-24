import geoip2.database
from django.conf import settings

def get_country_from_ip(request):
    ip = request.META.get('REMOTE_ADDR')

    try:
        reader = geoip2.database.Reader(settings.GEOIP_PATH)
        response = reader.country(ip)
        country_code = response.country.iso_code
        reader.close()
        return country_code
    except Exception as e:
        return None
