from django.conf import settings

def global_settings(request):
    # return any necessary values
    return {
        'FACILITY_NAME': settings.FACILITY_NAME,
        'FACILITY_ADDRESS': settings.FACILITY_ADDRESS,
        'FACILITY_EMAIL': settings.FACILITY_EMAIL,
        'FACILITY_PHONE': settings.FACILITY_PHONE,
    }