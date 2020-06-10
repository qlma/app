from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    recipients = models.ManyToManyField(User, related_name="recipients")
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('messaging:message-detail', kwargs={'pk': self.pk})