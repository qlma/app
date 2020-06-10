from django.shortcuts import get_object_or_404, render
from django.views import generic

from .models import School, Event
from django.contrib.auth.models import Group

from django.shortcuts import redirect
from .decorators import unacthenticated_user, allowed_users
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import (
    ListView,
    DetailView,
)

class GroupListView(LoginRequiredMixin, ListView):
    model = Group
    template_name = 'groups.html'
    context_object_name = 'groups'

    def get_queryset(self):
        groups = Group.objects.all()
        return groups

class GroupDetailView(LoginRequiredMixin, DetailView):
    model = Group



@unacthenticated_user
def redirect_login(request):
    response = redirect('/login')
    return response

def about(request):
    return render(request, 'about.html', {'title': 'About'})

@allowed_users(allowed_roles=['staff'])
def staff(request):
    return render(request, 'staff.html', {'title': 'Staff'})





def school(request, school_id):
    school = get_object_or_404(School, pk=school_id)
    return render(request, 'school.html', {'school': school})

def about(request):
    return render(request, 'about.html', {'title': 'About'})

def timetable(request):
    return render(request, 'timetable.html', {'title': 'Timetable'})

def help(request):
    return render(request, 'help.html', {'title': 'Help'})
