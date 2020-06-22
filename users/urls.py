from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from . import views

from .views import (
    GroupListView,
    GroupDetailView,
)

urlpatterns = [

    path('add_user', views.add_user, name="add_user"),
    path('add_user_save', views.add_user_save, name="add_user_save"),
    path('users', views.users, name="users"),
    path('edit_user/<str:user_id>', views.edit_user, name="edit_user"),
    path('edit_user_save', views.edit_user_save, name="edit_user_save"),
        
    path('groups/', GroupListView.as_view(), name='groups'),
    path('group/<int:pk>/', GroupDetailView.as_view(), name='group-detail'),

]