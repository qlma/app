from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile
from users.models import CustomUser

@receiver(post_save, sender=CustomUser)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        instance.profile.save()
