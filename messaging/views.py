import json
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    DeleteView,
)
from users.models import CustomUser
from .models import Message
from .forms import MessageForm

class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'messaging/messages_received.html'
    context_object_name = 'messaging'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(CustomUser, username=self.request.user)
        return Message.objects.filter(recipients=user).order_by('-date_posted')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(CustomUser, username=self.request.user)
        context['count'] = Message.objects.filter(recipients=user).filter(is_read=False).count()
        return context

class MessageSentListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'messaging/messages_sent.html'
    context_object_name = 'messaging'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(CustomUser, username=self.request.user)
        return Message.objects.filter(sender=user).order_by('-date_posted')

class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message

    def get_object(self):
        message = super().get_object()
        message.is_read = True
        message.save()
        return message

class MessageCreateView(LoginRequiredMixin, CreateView):

    model = Message
    fields = ['recipients', 'title', 'content']

    def get(self, request, *args, **kwargs):
        context = {'messageForm': MessageForm()}
        return render(request, 'messaging/message_form.html', context)

    def form_valid(self, form):
        form.instance.sender = self.request.user
        return super().form_valid(form)

class MessageReplyView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    fields = ['recipients', 'title', 'content']

    def get(self, request, pk, *args, **kwargs):
        message = get_object_or_404(Message, pk=pk)
        initial_dict = {
        #    'recipients': [(c.pk, c.username) for c in CustomUser.objects.filter(username=message.sender)],
        #    'title': 'Reply: ' + message.title
        }
        messageForm = MessageForm(initial = initial_dict)
        context = {}
        context['messageForm'] = messageForm
        return render(request, 'messaging/message_form.html', context)

class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('messaging:messages-received')

def search(request):
    if request.is_ajax():
        query = request.GET.get("term", "")
        try:
            users = CustomUser.objects.filter(
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

        