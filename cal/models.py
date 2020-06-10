from django.db import models
from django.urls import reverse

# Create your models here.

class Event(models.Model):
    category = models.CharField(max_length=10)
    title = models.CharField(max_length=200)
    description = models.TextField(u'description', help_text=u'Event description')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    @property
    def get_html_url(self):
        url = reverse('cal:event', args=(self.id,))
        cat = ''
        if self.category == '1':
            cat = 'school'
        if self.category == '2':
            cat = 'grade'
        return f'<a href="{url}" class="{cat}">{self.title}</a>'
