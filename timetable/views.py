import datetime
from itertools import cycle
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from project.decorators import unacthenticated_user, allowed_user_types
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from users.models import CustomUser
from .models import Course, Subject, Lesson

from django.views.generic import (
    View
)


class TimetableView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(CustomUser, username=request.user)
        groups = user.groups.all()
        if(groups):
            for group in groups:
                current_group = group # TODO: Get this from user session when multiple exists

            weekdays = [0,1,2,3,4]
            hours = ['08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00']
            lessons = Lesson.objects.filter(group_id=group.id)

            return render(request, 'timetable.html',
                {
                    'title': 'Timetable',
                    'current_group': current_group,
                    'hours': hours,
                    'weekdays': weekdays,
                    'lessons': lessons
                })
        else:
            messages.error(request, "Feature is not available. User is not assigned to a group.")
            return HttpResponseRedirect(reverse("news"))

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




def add_lesson(request):
    courses=Course.objects.all()
    WEEKDAYS = (
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    )
    HOURS = (
        (0, '08'),
        (1, '09'),
        (2, '10'),
        (3, '11'),
        (4, '12'),
        (5, '13'),
        (6, '14'),
        (7, '15'),
        (8, '16'),
        (9, '17'),
    )
    MINUTES = (
        (0, '00'),
        (1, '15'),
        (2, '30'),
    )
    groups=Group.objects.all()
    return render(request, "add_lesson.html", {"courses":courses, "groups": groups, "days":WEEKDAYS, "hours": HOURS, "minutes": MINUTES})

def add_lesson_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        course_id=request.POST.get("course")
        course=Course.objects.get(id=course_id)

        group_id=request.POST.get("group")
        group=Group.objects.get(id=group_id)
        
        weekday=request.POST.get("weekday")
        
        starts_at_hour=int(request.POST.get("starts_at_hour"))
        starts_at_minute=int(request.POST.get("starts_at_minute"))
        ends_at_hour=int(request.POST.get("ends_at_hour"))
        ends_at_minute=int(request.POST.get("ends_at_minute"))

        starts_at = datetime.time(starts_at_hour, starts_at_minute, 0)
        ends_at = datetime.time(ends_at_hour, ends_at_minute, 0)

        try:
            lesson_model=Lesson(course_id=course, group_id=group, weekday=weekday, starts_at=starts_at, ends_at=ends_at)
            lesson_model.save()
            messages.success(request,"Successfully Added Lesson")
            return HttpResponseRedirect(reverse("timetable:add_lesson"))
        except:
            messages.error(request,"Failed To Add Lesson")
            return HttpResponseRedirect(reverse("timetable:add_lesson"))

def manage_lessons(request):
    lessons=Lesson.objects.all()
    return render(request,"manage_lessons.html", {"lessons":lessons})

def edit_lesson(request, lesson_id):
    lesson=Lesson.objects.get(id=lesson_id)
    courses=Course.objects.all()
    groups=Group.objects.all()
    WEEKDAYS = (
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    )
    HOURS = (
        (0, '08'),
        (1, '09'),
        (2, '10'),
        (3, '11'),
        (4, '12'),
        (5, '13'),
        (6, '14'),
        (7, '15'),
        (8, '16'),
        (9, '17'),
    )
    MINUTES = (
        (0, '00'),
        (1, '15'),
        (2, '30'),
    )  
    return render(request,"edit_lesson.html", {"lesson":lesson, "courses":courses, "groups": groups, "days":WEEKDAYS, "hours": HOURS, "minutes": MINUTES})

def edit_lesson_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        lesson_id=request.POST.get("lesson_id")
        group_id=request.POST.get("group")
        course_id=request.POST.get("course")
        weekday=request.POST.get("weekday")

        starts_at_hour=int(request.POST.get("starts_at_hour"))
        starts_at_minute=int(request.POST.get("starts_at_minute"))
        ends_at_hour=int(request.POST.get("ends_at_hour"))
        ends_at_minute=int(request.POST.get("ends_at_minute"))

        starts_at = datetime.time(starts_at_hour, starts_at_minute, 0)
        ends_at = datetime.time(ends_at_hour, ends_at_minute, 0)

        try:
            lesson=Lesson.objects.get(id=lesson_id)
            group=Group.objects.get(id=group_id)
            lesson.group_id=group
            course=Course.objects.get(id=course_id)
            lesson.course_id=course
            lesson.weekday=int(weekday)
            print("weekday", weekday)
            lesson.starts_at=starts_at
            lesson.ends_at=ends_at
            lesson.save()
            messages.success(request,"Successfully Edited Lesson")
            return HttpResponseRedirect(reverse("timetable:edit_lesson", kwargs={"lesson_id":lesson_id}))
        except:
            messages.error(request,"Failed to Edit Lesson")
            return HttpResponseRedirect(reverse("timetable:edit_lesson", kwargs={"lesson_id":lesson_id}))