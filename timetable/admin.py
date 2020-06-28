from django.contrib import admin
from .models import Course, Subject, Lesson

# Register your models here.
admin.site.register(Course)
admin.site.register(Subject)
admin.site.register(Lesson)