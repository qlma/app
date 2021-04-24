from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [

    path('add_user', views.UserCreateView.as_view(), name="add_user"),
    path('edit_user/<str:user_id>', views.UserEditView.as_view(), name="edit_user"),
    
    path('manage_users', views.UsersManageView.as_view(), name="manage_users"),
    path('manage_groups', views.GroupListView.as_view(), name='manage_groups'),
    path('add_group', views.GroupCreateView.as_view(), name='add_group'),
    path('edit_group/<int:group_id>/', views.GroupEditView.as_view(), name='edit_group'),
    path('delete_group/<int:group_id>/', views.GroupDeleteView.as_view(), name='delete_group'),

    path('groups/', views.GroupsView.as_view(), name='groups'),

]