import datetime
from itertools import cycle
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.views import generic
from users.models import CustomUser
from .models import Lunch
from .forms import LunchForm

from project.decorators import unacthenticated_user, allowed_user_types

@login_required
@allowed_user_types(allowed_roles=['Teacher', 'Admin'])
def index(request):
    username = request.user
    user=CustomUser.objects.get(username=username)
    lunches = Lunch.objects.all()
    return render(request, 'lunches.html',
        {
            'title': 'Lunch menu',
            'lunches': lunches
        })

@allowed_user_types(allowed_roles=['Teacher', 'Admin'])
def add_lunch(request):
    if request.method=="GET":
        lunchForm = LunchForm()
        lunches=Lunch.objects.all()
        return render(request, "add_lunch.html", {'lunchForm' : lunchForm})
    else:
        lunchForm = LunchForm(request.POST)
        if lunchForm.is_valid():
            try:
                lunch=Lunch()
                lunch.date = lunchForm.cleaned_data['date']
                lunch.title = lunchForm.cleaned_data['title']
                lunch.description = lunchForm.cleaned_data['description']
                lunch.save()
                messages.success(request,"Successfully Added Lunch")
                return HttpResponseRedirect(reverse("lunch:add_lunch"))
            except:
                messages.error(request,"Failed To Add Lunch")
                return HttpResponseRedirect(reverse("lunch:add_lunch"))

@allowed_user_types(allowed_roles=['Teacher', 'Admin'])
def manage_lunches(request):
    lunches=Lunch.objects.all()
    return render(request,"manage_lunches.html", {"lunches":lunches})

@allowed_user_types(allowed_roles=['Teacher', 'Admin'])
def edit_lunch(request,lunch_id):
    lunch=Lunch.objects.get(id=lunch_id)
    if request.method=="GET":
        lunchForm = LunchForm(
            initial={
                'title': lunch.title,
                'description': lunch.description
            }
        )
        return render(request,"edit_lunch.html", {"lunch": lunch, "lunchForm":lunchForm})
    else:
        lunchForm = LunchForm(request.POST)
        if lunchForm.is_valid():
            try:
                lunch.date = lunchForm.cleaned_data['date']
                lunch.title = lunchForm.cleaned_data['title']
                lunch.description = lunchForm.cleaned_data['description']
                lunch.save()
                messages.success(request,"Successfully Edited Lunch")
                return HttpResponseRedirect(reverse("lunch:edit_lunch", kwargs={"lunch_id":lunch_id}))
            except:
                messages.error(request,"Failed to Edit Lunch")
                return HttpResponseRedirect(reverse("lunch:edit_course", kwargs={"lunch_id":lunch_id}))
        else:
            messages.error(request,"Invalid data")
            return HttpResponseRedirect(reverse("lunch:edit_course", kwargs={"lunch_id":lunch_id}))

@allowed_user_types(allowed_roles=['Teacher', 'Admin'])
def delete_lunch(request,lunch_id):
    if request.method == 'GET':
        lunch=Lunch.objects.get(id=lunch_id)
        lunch.delete()
        messages.success(request,"Successfully deleted Lunch")
        return HttpResponseRedirect(reverse("lunch:manage_lunches"))