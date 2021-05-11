from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import Group
from django.views import generic
from django.views.generic import (
    ListView,
)
from project.utils import is_staff, is_author

from .models import School, Event

class RedirectLoginView(LoginRequiredMixin, ListView):
    def get(self, request):
        return redirect('/login')

class StaffView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    def get(self, request):
        return render(request, 'staff.html', {'title': 'Staff'})

    def test_func(self):
        return is_staff(self)

def about(request):
    return render(request, 'about.html', {'title': 'About'})

def school(request, school_id):
    school = get_object_or_404(School, pk=school_id)
    return render(request, 'school.html', {'school': school})

def about(request):
    return render(request, 'about.html', {'title': 'About'})

def help(request):
    return render(request, 'help.html', {'title': 'Help'})
