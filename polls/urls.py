from django.urls import path

from . import views

app_name = 'polls'

urlpatterns = [
    
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),

    path('manage_polls/', views.ManagePollsView.as_view(), name='manage_polls'),
    path('add_poll', views.add_poll, name="add_poll"),
    path('edit_poll/<str:question_id>', views.edit_poll, name="edit_poll"),
    path('delete_poll/<str:question_id>', views.delete_poll, name="delete_poll"),
    
]
