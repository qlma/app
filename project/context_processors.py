from django.conf import settings

def global_settings(request):
    # return any necessary values
    return {
        'FACILITY_NAME': settings.FACILITY_NAME,
        'FACILITY_LOCATION': settings.FACILITY_LOCATION
    }