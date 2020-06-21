from django.db import models

# Create your models here.

class School(models.Model):
    name = models.CharField('School Name', max_length=120)
    address = models.CharField('Address', max_length=120)
    code = models.CharField('School Code', max_length=12)
    principal = models.CharField('Principal Name', max_length=120)
    email_address = models.EmailField('Email Address')
    phone = models.CharField('Contact Phone', max_length=20)
    web = models.URLField('Web Address')

    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField('Event Name', max_length=120)
    event_date = models.DateTimeField('Event Date')
    venue = models.CharField(max_length=120)
    organizer = models.CharField(max_length = 60)
    description = models.TextField(blank=True)
 
    def __str__(self):
        return self.name

