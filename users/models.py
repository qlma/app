from django.contrib.auth.models import AbstractUser

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from PIL import Image


class CustomUser(AbstractUser):
    USER_TYPES = (
        ('1', 'Student'),
        ('2', 'Teacher'),
        ('3', 'Parent'),
        ('4', 'Admin')
    )
    user_type = models.CharField(choices=USER_TYPES, default=1, max_length=1)

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    address=models.CharField(max_length=150)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

