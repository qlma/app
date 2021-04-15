from django import forms
from django.forms import ModelForm, TextInput, DateInput
from lunch.models import Lunch

class LunchForm(forms.ModelForm):
    date = forms.DateField(
        input_formats=['%Y-%m-%d'],
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'id': 'picker_date',
                'class': 'datepicker',
                'placeholder':'Select a date'
            }
        )
    )
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Tasty tacos'
            }
        )
    )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'rows':5,
                'cols':20,
                'id': 'summernote',
                'class': 'form-control',
                'placeholder': 'Lunch consists of the following ingredients.'
            }
        )
    )

    class Meta:
        model = Lunch
        fields = ['date', 'title', 'description']

    def __init__(self, *args, **kwargs):
        super(LunchForm, self).__init__(*args, **kwargs)
