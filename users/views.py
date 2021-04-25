import os
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.urls import reverse
from django.contrib import messages
from users.models import CustomUser, Profile
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, GroupForm
from project.decorators import unacthenticated_user, allowed_user_types
from django.utils.decorators import method_decorator

from django.contrib.auth import login as auth_login
from django.contrib.auth.views import LoginView

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
    UpdateView,
    CreateView,
    DeleteView
)

from users.forms import UserLoginForm

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
            messages.error(request,"User is not assigned to a group. Some features are not available.")
            return redirect('news')
        else:
            messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('login')

class LoginView(LoginView):
    template_name = 'users/login.html'
    authentication_form = UserLoginForm

    def post(self, request):
        username = request.POST.get('username')
        try:
            user = CustomUser.objects.get(username=username)
        except:
            user = None

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse("news"))
            else:
                messages.error(request, ('Account is inactive.'))
                return HttpResponseRedirect(reverse("login"))
        else:
            messages.error(request, ('Please check your username.'))
            return redirect("login")


class GroupsView(ListView):
    def get(self, request):
        user = get_object_or_404(CustomUser, username=self.request.user)
        groups = user.groups.all()
        if(groups):
            all_groups=Group.objects.all()
            return render(request,"groups/groups.html", { "groups": all_groups })
        else:
            messages.error(request, "Feature is not available. User is not assigned to a group.")
            return HttpResponseRedirect(reverse("news"))

class ProfileView(LoginRequiredMixin, View):

    def get(self, request):
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        context = {
            'u_form': u_form,
            'p_form': p_form
        }
        return render(request, 'users/profile.html', context)

    def post(self, request):
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                request.FILES,
                                instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

class UserDetailView(DetailView):
    def get(self, request, username, *args, **kwargs):
        user = get_object_or_404(CustomUser, username=username)
        context = {
            'user': user
        }
        return render(request, 'users/user.html', context)

class UsersManageView(LoginRequiredMixin, ListView):
    @method_decorator(allowed_user_types(allowed_roles=['Teacher', 'Admin']))
    def get(self, request, *args, **kwargs):
        users=CustomUser.objects.all()
        return render(request,"admin/manage_users.html", { "users": users })

class UserCreateView(LoginRequiredMixin, CreateView):
    @method_decorator(allowed_user_types(allowed_roles=['Teacher', 'Admin']))
    def get(self, request, *args, **kwargs):
        return render(request,"admin/add_user.html")

    @method_decorator(allowed_user_types(allowed_roles=['Teacher', 'Admin']))
    def post(self, request, *args, **kwargs):
        try:
            user=CustomUser.objects.create_user(
                username=request.POST.get("username"),
                password=request.POST.get("password"),
                first_name=request.POST.get("first_name"),
                last_name=request.POST.get("last_name"),
                email=request.POST.get("email"))
            user.save()
            messages.success(request, "Successfully Added User")
            return HttpResponseRedirect(reverse("add_user"))
        except:
            messages.error(request,"Failed to Add User")
            return HttpResponseRedirect(reverse("add_user"))

class UserEditView(LoginRequiredMixin, UpdateView):
    @method_decorator(allowed_user_types(allowed_roles=['Teacher', 'Admin']))
    def get(self, request, user_id, *args, **kwargs):
        user=CustomUser.objects.get(id=user_id)
        profile=Profile.objects.get(user=user)
        groups = Group.objects.all()
        return render(request,"admin/edit_user.html",{ "user":user, "profile":profile , "user_id":user_id, "groups": groups })

    @method_decorator(allowed_user_types(allowed_roles=['Teacher', 'Admin']))
    def post(self, request, user_id, *args, **kwargs):
        try:
            user=CustomUser.objects.get(id=user_id)
            user.first_name=request.POST.get("first_name")
            user.last_name=request.POST.get("last_name")
            user.email=request.POST.get("email")
            user.username=request.POST.get("username")

            user.groups.clear()
            group_id = request.POST.get("group_id")
            if group_id != "":    
                g = Group.objects.get(id=group_id)
                g.user_set.add(user)

            user.is_staff=request.POST.get("is_staff", "") == 'on'
            user.is_active=request.POST.get("is_active", "") == 'on'
            user.save()

            profile=Profile.objects.get(user=user)
            profile.address=request.POST.get("address")
            profile.save()

            messages.success(request,"Successfully Edited User")
            return HttpResponseRedirect(reverse("edit_user", kwargs={"user_id":user_id}))
        except:
            messages.error(request,"Failed to Edit User")
            return HttpResponseRedirect(reverse("edit_user", kwargs={"user_id":user_id}))

class GroupListView(LoginRequiredMixin, ListView):
    @method_decorator(allowed_user_types(allowed_roles=['Teacher', 'Admin']))
    def get(self, request, *args, **kwargs):
        users_without_group=CustomUser.objects.filter(groups__isnull=True)
        groups=Group.objects.all()
        return render(request,"admin/manage_groups.html", { "users_without_group": users_without_group, "groups": groups })

class GroupCreateView(LoginRequiredMixin, CreateView):
    @method_decorator(allowed_user_types(allowed_roles=['Teacher', 'Admin']))
    def get(self, request, *args, **kwargs):
        return render(request,"admin/add_group.html")

    @method_decorator(allowed_user_types(allowed_roles=['Teacher', 'Admin']))
    def post(self, request, *args, **kwargs):
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

class GroupEditView(LoginRequiredMixin, UpdateView):
    @method_decorator(allowed_user_types(allowed_roles=['Teacher', 'Admin']))
    def get(self, request, group_id, *args, **kwargs):
        group = get_object_or_404(Group, id=group_id)
        users = CustomUser.objects.filter(groups__name=group.name)
        return render(request,"admin/edit_group.html", { "group": group, "users": users })

class GroupDeleteView(LoginRequiredMixin, DeleteView):
    @method_decorator(allowed_user_types(allowed_roles=['Teacher', 'Admin']))
    def get(self, request, group_id, *args, **kwargs):
        group = get_object_or_404(Group, id=group_id)
        group.delete()
        messages.success(request,"Successfully deleted group")
        return HttpResponseRedirect(reverse("manage_groups"))

