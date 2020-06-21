from django.contrib import admin

from .models import School, Event

# Register your models here.
admin.site.register(School)
admin.site.register(Event)