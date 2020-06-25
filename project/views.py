from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import Group
from django.views import generic

from .models import School, Event
from .decorators import unacthenticated_user, allowed_user_types



@unacthenticated_user
def redirect_login(request):
    response = redirect('/login')
    return response

def about(request):
    return render(request, 'about.html', {'title': 'About'})

@allowed_user_types(allowed_roles=['Teacher', 'Admin'])
def staff(request):
    return render(request, 'staff.html', {'title': 'Staff'})


def school(request, school_id):
    school = get_object_or_404(School, pk=school_id)
    return render(request, 'school.html', {'school': school})

def about(request):
    return render(request, 'about.html', {'title': 'About'})

def help(request):
    return render(request, 'help.html', {'title': 'Help'})
