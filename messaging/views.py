import json
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
)
from .models import Message

class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'messaging/messaging.html'
    context_object_name = 'messaging'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user)
        return Message.objects.filter(recipients=user).order_by('-date_posted')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.request.user)
        context['count'] = Message.objects.filter(recipients=user).filter(is_read=False).count()
        return context

class MessageSentListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'messaging/sent_messages.html'
    context_object_name = 'messaging'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.request.user)
        return Message.objects.filter(sender=user).order_by('-date_posted')

class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message

    def get_object(self):
        obj = super().get_object()
        obj.is_read = True
        obj.save()
        return obj

class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    fields = ['recipients', 'title', 'content']

    def form_valid(self, form):
        form.instance.sender = self.request.user
        return super().form_valid(form)


def search(request):
    if request.is_ajax():
        query = request.GET.get("term", "")
        try:
            users = User.objects.filter(
                        Q(username__istartswith=query) |
                        Q(first_name__istartswith=query) |
                        Q(last_name__istartswith=query)
                    ).order_by('username')
        except error:
            messages.add_message(request, messages.ERROR, error)
    return HttpResponse(get_recipient_list(users), 'application/json')

def get_recipient_list(users):
    result = []
    for user in users:
        option = { 'id': user.id, 'label': user.first_name + ' ' +  user.last_name + ' (' + user.username + ')' }
        result.append(option)
    return json.dumps(result)