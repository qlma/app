from django import forms
from django.forms import ModelForm, DateTimeInput, FileField
from cal.models import Event

class EventForm(ModelForm):
  title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
  category = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
  description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

  class Meta:
    model = Event
    # datetime-local is a HTML5 input type, format to make date time show on fields
    widgets = {
      'start_time': DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
      'end_time': DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
    }
    fields = ['title', 'category', 'description', 'start_time', 'end_time']

  def __init__(self, *args, **kwargs):
    super(EventForm, self).__init__(*args, **kwargs)
    # input_formats parses HTML5 datetime-local input to datetime field
    self.fields['start_time'].input_formats = ['%Y-%m-%dT%H:%M',]
    self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)

class IcalForm(forms.Form):
  icsfile = FileField(
      label='Select a file',
      help_text='max. 42 megabytes'
  )
