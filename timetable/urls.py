from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views

from . import views

app_name = 'timetable'

urlpatterns = [
    path('timetable/', views.timetable, name='timetable'),
    path('add_course', views.add_course, name="add_course"),
    path('add_course_save', views.add_course_save, name="add_course_save"),
    path('courses', views.courses, name="courses"),
]
