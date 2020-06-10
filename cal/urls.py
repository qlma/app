#from django.urls import path, re_path
from django.conf.urls import url

from . import views


app_name = 'cal'

urlpatterns = [
    url(r'^index/$', views.index, name='index'),
    url(r'^calendar/$', views.CalendarView.as_view(), name='calendar'),
    url(r'^event/new/$', views.event, name='event_new'),
	url(r'^event/(?P<event_id>\d+)/$', views.event, name='event'),
    url('ical/', views.ical, name='ical'),

]