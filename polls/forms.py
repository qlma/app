from django import forms
from django.forms import ModelForm, TextInput
from polls.models import Choice, Question

class PollForm(forms.ModelForm):
    question_text = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Question
        exclude = ['pub_date']

    def __init__(self, *args, **kwargs):
        super(PollForm, self).__init__(*args, **kwargs)
