from django import forms
from django.forms import ModelForm, TextInput, Textarea, DateInput, DateTimeInput, FileField
from cal.models import Event

class EventForm(forms.ModelForm):
  title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
  category = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
  description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
  start_time = forms.DateTimeField(
    input_formats=['%Y-%m-%d %H:%M'],
    widget=forms.DateTimeInput(
      attrs={
        'id': 'picker_start_time',
        'class': 'form-control',
      }
    )
  )
  end_time = forms.DateTimeField(
    input_formats=['%Y-%m-%d %H:%M'],
    widget=forms.DateTimeInput(
      attrs={
        'id': 'picker_end_time',
        'class': 'form-control',
      }
    )
  )
  class Meta:
    model = Event
    fields = "__all__"

  def __init__(self, *args, **kwargs):
    super(EventForm, self).__init__(*args, **kwargs)

class IcalForm(forms.Form):
  icsfile = FileField(
      label='Select a file',
      help_text='max. 42 megabytes'
  )
