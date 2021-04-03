#from django.urls import path, re_path
from django.conf.urls import url
from django.urls import path

from . import views


app_name = 'cal'

urlpatterns = [
    url(r'^index/$', views.index, name='index'),
    url(r'^calendar/$', views.CalendarView.as_view(), name='calendar'),
    url(r'^event/new/$', views.event, name='event_new'),
	url(r'^event/(?P<event_id>\d+)/$', views.event, name='event'),
    url('ical/', views.ical, name='ical'),

    path('manage_events', views.manage_events, name="manage_events"),
    path('add_event', views.add_event, name="add_event"),
    path('edit_event/<str:event_id>', views.edit_event, name="edit_event"),
    path('delete_event/<str:event_id>', views.delete_event, name="delete_event"),

]