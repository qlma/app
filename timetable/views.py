from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.views import generic
from users.models import CustomUser
from .models import Course, Subject


def timetable(request):
    return render(request, 'timetable.html', {'title': 'Timetable'})

def add_course(request):
    subjects=Subject.objects.all()
    staffs=CustomUser.objects.filter(user_type=2)
    return render(request, "add_course.html", {"staffs":staffs, "subjects":subjects})

def add_course_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        course_name=request.POST.get("course")
        subject_id=request.POST.get("subject")
        subject=Subject.objects.get(id=subject_id)
        staff_id=request.POST.get("staff")
        staff=CustomUser.objects.get(id=staff_id)

        try:
            course_model=Course(name=course_name, subject_id=subject, staff_id=staff)
            course_model.save()
            messages.success(request,"Successfully Added Course")
            return HttpResponseRedirect(reverse("timetable:add_course"))
        except:
            messages.error(request,"Failed To Add Course")
            return HttpResponseRedirect(reverse("timetable:add_course"))

def manage_courses(request):
    courses=Course.objects.all()
    return render(request,"manage_courses.html", {"courses":courses})

def edit_course(request,course_id):
    course=Course.objects.get(id=course_id)
    subjects=Subject.objects.all()
    staffs=CustomUser.objects.filter(user_type=2)
    return render(request,"edit_course.html", {"course":course, "subjects":subjects, "staffs":staffs})

def edit_course_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        course_id=request.POST.get("course_id")
        course_name=request.POST.get("course")
        subject_id=request.POST.get("subject")
        staff_id=request.POST.get("staff")

        try:
            course=Course.objects.get(id=course_id)
            course.name=course_name
            subject=Subject.objects.get(id=subject_id)
            course.subject_id=subject
            staff=CustomUser.objects.get(id=staff_id)
            course.staff_id=staff
            course.save()
            messages.success(request,"Successfully Edited Course")
            return HttpResponseRedirect(reverse("timetable:edit_course", kwargs={"course_id":course_id}))
        except:
            messages.error(request,"Failed to Edit Course")
            return HttpResponseRedirect(reverse("timetable:edit_course", kwargs={"course_id":course_id}))

def add_subject(request):
    return render(request,"add_subject.html")

def add_subject_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        subject_name=request.POST.get("subject_name")
        try:
            subject=Subject(subject_name=subject_name)
            subject.save()
            messages.success(request,"Successfully Added Subject")
            return HttpResponseRedirect(reverse("timetable:add_subject"))
        except:
            messages.error(request,"Failed to Add Subject")
            return HttpResponseRedirect(reverse("timetable:add_subject"))

def edit_subject(request,subject_id):
    subject=Subject.objects.get(id=subject_id)
    courses=Course.objects.all()
    staffs=CustomUser.objects.filter(user_type=2)
    return render(request,"edit_subject.html", {"subject":subject, "staffs":staffs, "courses":courses, "id":subject_id})

def edit_subject_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        subject_id=request.POST.get("subject_id")
        subject_name=request.POST.get("subject_name")

        try:
            subject=Subject.objects.get(id=subject_id)
            subject.subject_name=subject_name
            subject.save()

            messages.success(request,"Successfully Edited Subject")
            return HttpResponseRedirect(reverse("timetable:edit_subject", kwargs={"subject_id":subject_id}))
        except:
            messages.error(request,"Failed to Edit Subject")
            return HttpResponseRedirect(reverse("timetable:edit_subject", kwargs={"subject_id":subject_id}))

def manage_subjects(request):
    subjects=Subject.objects.all()
    return render(request,"manage_subjects.html", {"subjects":subjects})