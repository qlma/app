from django import forms
from .models import Post
from django.forms import CharField

class NewsForm(forms.ModelForm):

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
        model = Post
        fields = ['title', 'content']
        
    def __init__(self, *args, user_id=None, **kwargs):
        super(NewsForm, self).__init__(*args, **kwargs)
        

