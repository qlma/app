from django import forms
from .models import Message
from django.shortcuts import get_object_or_404
from users.models import CustomUser
from django.forms import CharField, MultipleChoiceField, TextInput, SelectMultiple

class MessageForm(forms.ModelForm):

    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'rows':5,
                'cols':20,
                'id': 'summernote',
                'class': 'form-control',
                'placeholder': ''
            }
        )
    )

    class Meta:
        model = Message
        fields = ['recipients', 'title', 'content']
        
    def __init__(self, *args, user_id=None, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        
        
