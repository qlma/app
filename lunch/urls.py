from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views

from . import views

app_name = 'lunch'

urlpatterns = [
    path('', views.index, name='index'),

    path('manage_lunches', views.manage_lunches, name="manage_lunches"),
    path('add_lunch', views.add_lunch, name="add_lunch"),
    path('edit_lunch/<str:lunch_id>', views.edit_lunch, name="edit_lunch"),
    path('delete_lunch/<str:lunch_id>', views.delete_lunch, name="delete_lunch"),
    path('detail/<str:lunch_id>', views.detail, name="detail"),

]
