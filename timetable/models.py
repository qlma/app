from django.contrib.auth.models import AbstractUser

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models

class Course(models.Model):
    name = models.CharField('Course Name', max_length=120)