from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from users.models import CustomUser
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from project.decorators import unacthenticated_user, allowed_user_types
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import (
    ListView,
    DetailView,
)

from django.urls import reverse

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

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
            user=CustomUser.objects.create_user(username=username,password=password,first_name=first_name,last_name=last_name,email=email,address=address)
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
def manage_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    users = CustomUser.objects.filter(groups__name=group.name)
    return render(request,"admin/manage_group.html", { "group": group, "users": users })

def groups(request):
    groups=Group.objects.all()
    return render(request,"groups/groups.html", { "groups": groups })