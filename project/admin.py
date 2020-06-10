from django.contrib import admin

from .models import School, Group, Event

# Register your models here.
admin.site.register(School)
admin.site.register(Group)
admin.site.register(Event)