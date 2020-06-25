from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.views import generic
from .models import Course


def timetable(request):
    return render(request, 'timetable.html', {'title': 'Timetable'})

def add_course(request):
    return render(request, "add_course.html")

def add_course_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        course=request.POST.get("course")
        try:
            course_model=Course(name=course)
            course_model.save()
            messages.success(request,"Successfully Added Course")
            return HttpResponseRedirect(reverse("timetable:add_course"))
        except:
            messages.error(request,"Failed To Add Course")
            return HttpResponseRedirect(reverse("timetable:add_course"))

def courses(request):
    courses=Course.objects.all()
    return render(request, "courses.html", {'courses': courses})