from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [

    path('add_user', views.add_user, name="add_user"),
    path('add_user_save', views.add_user_save, name="add_user_save"),
    path('edit_user/<str:user_id>', views.edit_user, name="edit_user"),
    path('edit_user_save', views.edit_user_save, name="edit_user_save"),
    
    path('manage_users', views.manage_users, name="manage_users"),
    path('manage_groups', views.manage_groups, name='manage_groups'),
    path('manage_group/<int:group_id>/', views.manage_group, name='manage_group'),
    path('groups/', views.groups, name='groups'),

]