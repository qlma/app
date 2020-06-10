from datetime import datetime, timedelta, date
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.safestring import mark_safe
from django.views import generic
from icalendar import Calendar
import calendar

from .models import Event

from .utils import TermCalendar
from .forms import EventForm
from .forms import IcalForm

from django.views.generic import (
    ListView,
)


# Create your views here.

def index(request):
    return HttpResponse('hello')

class CalendarView(ListView):
    model = Event
    template_name = 'cal/calendar.html'
    success_url = reverse_lazy("calendar")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = TermCalendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

def event(request, event_id=None):
    event = Event()
    if event_id:
        event = get_object_or_404(Event, pk=event_id)
    else:
        event = Event()
    return render(request, 'cal/event.html', {'event': event})



def ical(request):

    if request.method == 'POST':
        
        # Get posted file
        form = IcalForm(request.POST, request.FILES)
        if form.is_valid():
            category = request.POST['category']
            icsfile = request.FILES['icsfile']

            # Remove all events from database
            Event.objects.filter(category=category).delete()

            # Read the .ics file
            cal = Calendar.from_ical(icsfile.read())

            # Parse events
            events = []
            for element in cal.walk('vevent'):
                eventdict = {}
                if element.get('summary') != None:
                    eventdict['summary'] = element.get('summary')
                else:
                    eventdict['summary'] = ''
                if element.get('description') != None:
                    eventdict['description'] = element.get('description')
                else:
                    eventdict['description'] = ''
                if element.get('url') != None:
                    eventdict['url'] = element.get('url')
                else:
                    eventdict['url'] = ''
                if element.get('dtstart') != None:
                    eventdict['dtstart'] = element.get('dtstart').dt
                else:
                    eventdict['dtstart'] = ''
                if element.get('dtend') != None:
                    eventdict['dtend'] = element.get('dtend').dt
                else:
                    eventdict['dtend'] = ''

                events.append(eventdict)

                # Save all events to database
                event_model = Event(
                        category=category,
                        title=eventdict['summary'], 
                        description=eventdict['description'], 
                        start_time=eventdict['dtstart'], 
                        end_time=eventdict['dtend']
                    )
                event_model.save()

            messages.success(request, f'Calendar data uploaded succesfully')
            return render(request, 'cal/ical.html')
        else:
            form = IcalForm()

    return render(request, 'cal/ical.html')



