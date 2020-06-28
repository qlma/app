from django.contrib.auth.models import AbstractUser

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from users.models import CustomUser
from django.db import models

class Subject(models.Model):
    id=models.AutoField(primary_key=True)
    subject_name=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

    def __str__(self):
        return self.subject_name

class Course(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255)
    subject_id=models.ForeignKey(Subject, on_delete=models.CASCADE, default=1)
    staff_id=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

    def __str__(self):
        return self.name

class Lesson(models.Model):
    id=models.AutoField(primary_key=True)
    group_id=models.ForeignKey(Group, on_delete=models.CASCADE)
    course_id=models.ForeignKey(Course, on_delete=models.CASCADE)
    weekday=models.IntegerField()
    starts_at=models.TimeField()
    ends_at=models.TimeField()
    objects=models.Manager()

    def __str__(self):
        return 'Lesson: {}'.format(self.id)

