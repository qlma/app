from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views

from . import views

from .views import (
    TimetableView,
)

app_name = 'timetable'

urlpatterns = [
    path('timetable/', views.TimetableView.as_view(), name='timetable'),

    path('manage_courses', views.manage_courses, name="manage_courses"),
    path('add_course', views.add_course, name="add_course"),
    path('add_course_save', views.add_course_save, name="add_course_save"),
    path('edit_course/<str:course_id>', views.edit_course, name="edit_course"),
    path('edit_course_save', views.edit_course_save, name="edit_course_save"),

    path('manage_subjects', views.manage_subjects, name="manage_subjects"),
    path('add_subject', views.add_subject,name="add_subject"),
    path('add_subject_save', views.add_subject_save,name="add_subject_save"),
    path('edit_subject/<str:subject_id>', views.edit_subject, name="edit_subject"),
    path('edit_subject_save', views.edit_subject_save, name="edit_subject_save"),
    
    path('manage_lessons', views.manage_lessons, name="manage_lessons"),
    path('add_lesson', views.add_lesson, name="add_lesson"),
    path('add_lesson_save', views.add_lesson_save, name="add_lesson_save"),
    path('edit_lesson/<str:lesson_id>', views.edit_lesson, name="edit_lesson"),
    path('edit_lesson_save', views.edit_lesson_save, name="edit_lesson_save"),
]
