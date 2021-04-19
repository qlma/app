from django import forms
from users.models import CustomUser
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from .models import Profile
from users.models import CustomUser
from django.forms import ModelChoiceField

class UserRegisterForm(UserCreationForm):

    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email']

class ProfileUpdateForm(forms.ModelForm):

    address = forms.CharField(max_length=150, required=False)

    class Meta:
        model = Profile
        fields = ['image', 'address']

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']
