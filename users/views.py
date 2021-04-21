import os
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from users.models import CustomUser
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, GroupForm
from project.decorators import unacthenticated_user, allowed_user_types
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import send_mail

from django.views.generic import (
    View,
    ListView,
    DetailView,
)

class RegisterView(View):
    form_class = UserRegisterForm
    template_name = 'users/register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            user = form.save(commit=False)
            user.is_active = False # Deactivate account till it is confirmed
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate Your Qlma Account'
            message = render_to_string('users/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            messages.success(request, ('Please Confirm your email to complete registration.'))
            return redirect('login')

        return render(request, self.template_name, {'form': form})


class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.profile.email_confirmed = True
            user.save()
            login(request, user)
            messages.success(request, ('Your account have been confirmed.'))
            return redirect('news')
        else:
            messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('login')

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)

def user(request, username):
    user = get_object_or_404(CustomUser, username=username)
    context = {
        'user': user
    }
    return render(request, 'users/user.html', context)

@allowed_user_types(allowed_roles=['Teacher', 'Admin'])
def manage_users(request):
    users=CustomUser.objects.all()
    return render(request,"admin/manage_users.html", { "users": users })

@allowed_user_types(allowed_roles=['Teacher', 'Admin'])
def add_user(request):
    return render(request,"admin/add_user.html")

@allowed_user_types(allowed_roles=['Teacher', 'Admin'])
def add_user_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        username=request.POST.get("username")
        password=request.POST.get("password")
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        email=request.POST.get("email")
        address=request.POST.get("address")

        try:
            user=CustomUser.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email,
                address=address)
            user.save()
            messages.success(request,"Successfully Added User")
            return HttpResponseRedirect(reverse("add_user"))
        except:
            messages.error(request,"Failed to Add User")
            return HttpResponseRedirect(reverse("add_user"))

@allowed_user_types(allowed_roles=['Teacher', 'Admin'])
def edit_user(request, user_id):
    user=CustomUser.objects.get(id=user_id)
    groups = Group.objects.all()
    return render(request,"admin/edit_user.html",{ "user":user, "user_id":user_id, "groups": groups })

@allowed_user_types(allowed_roles=['Teacher', 'Admin'])
def edit_user_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:

        user_id=request.POST.get("user_id")
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        email=request.POST.get("email")
        username=request.POST.get("username")
        address=request.POST.get("address")
        group_id = request.POST.get('group_id')

        try:    
        
            user=CustomUser.objects.get(id=user_id)
            user.first_name=first_name
            user.last_name=last_name
            user.email=email
            user.username=username
            user.address=address

            user.groups.clear()
            if group_id != "":    
                g = Group.objects.get(id=group_id)
                g.user_set.add(user)

            user.save()

            messages.success(request,"Successfully Edited User")
            return HttpResponseRedirect(reverse("edit_user", kwargs={"user_id":user_id}))
        except:
            messages.error(request,"Failed to Edit User")
            return HttpResponseRedirect(reverse("edit_user", kwargs={"user_id":user_id}))

@allowed_user_types(allowed_roles=['Teacher', 'Admin'])
def manage_groups(request):
    users_without_group=CustomUser.objects.filter(groups__isnull=True)
    groups=Group.objects.all()
    return render(request,"admin/manage_groups.html", { "users_without_group": users_without_group, "groups": groups })

@allowed_user_types(allowed_roles=['Teacher', 'Admin'])
def add_group(request):
    if request.method == 'GET':
        return render(request,"admin/add_group.html")
    if request.method == 'POST':
        groupForm = GroupForm(request.POST)
        if groupForm.is_valid():
            group = Group()
            group.name = groupForm.cleaned_data['name']
            group.save()

            messages.success(request,"Successfully added group")
            return HttpResponseRedirect(reverse("manage_groups"))
        else:
            messages.error(request,"Failed to add Group")
            return HttpResponseRedirect(reverse("add_group"))

@allowed_user_types(allowed_roles=['Teacher', 'Admin'])
def edit_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    users = CustomUser.objects.filter(groups__name=group.name)
    return render(request,"admin/edit_group.html", { "group": group, "users": users })

@allowed_user_types(allowed_roles=['Teacher', 'Admin'])
def delete_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    group.delete()
    messages.success(request,"Successfully deleted group")
    return HttpResponseRedirect(reverse("manage_groups"))

def groups(request):
    groups=Group.objects.all()
    return render(request,"groups/groups.html", { "groups": groups })