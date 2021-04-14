from django.contrib.auth.models import AbstractUser

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from users.models import CustomUser
from django.db import models

class Lunch(models.Model):
    id=models.AutoField(primary_key=True)
    date=models.DateField(max_length=255)
    title = models.TextField()
    description = models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description
