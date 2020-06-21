from django.shortcuts import get_object_or_404, render
from django.views import generic

from .models import School, Event
from django.contrib.auth.models import Group

from django.shortcuts import redirect
from .decorators import unacthenticated_user, allowed_user_types
from django.contrib.auth.mixins import LoginRequiredMixin
from users.models import CustomUser

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
    template_name = 'group_detail.html'
    context_object_name = 'users'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        group_id = self.kwargs.get('pk', None)
        group = get_object_or_404(Group, id=group_id)
        users = CustomUser.objects.filter(groups__name=group.name)
        context["users"] = users
        return context

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

def timetable(request):
    return render(request, 'timetable.html', {'title': 'Timetable'})

def help(request):
    return render(request, 'help.html', {'title': 'Help'})
