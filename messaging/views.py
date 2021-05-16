import json
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q
from django.contrib.auth.models import Group
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
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

    def get(self, request, *args, **kwargs):
        context = {}
        user = get_object_or_404(CustomUser, username=self.request.user)
        groups = user.groups.all()
        if(groups):
            context['messaging'] = Message.objects.filter(recipients=user, is_archived=False).order_by('-date_posted')
            context['unread_messages_count'] = Message.objects.filter(recipients=user).filter(is_read=False).count()
            return render(request, self.template_name, context)
        else:
            messages.error(request, "Feature is not available. User is not assigned to a group.")
            return HttpResponseRedirect(reverse("news"))

class MessageSentListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'messaging/messages_sent.html'
    context_object_name = 'messaging'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(CustomUser, username=self.request.user)
        return Message.objects.filter(sender=user).order_by('-date_posted')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(CustomUser, username=self.request.user)
        context['unread_messages_count'] = Message.objects.filter(recipients=user).filter(is_read=False).count()
        return context

class MessageDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Message

    def get_object(self):
        message = super().get_object()
        message.is_read = True
        message.save()
        return message

    def test_func(self):
        message = super().get_object()
        if self.request.user in message.recipients.all():
            return True
        return False

class MessageCreateView(LoginRequiredMixin, CreateView):

    model = Message
    fields = ['recipients', 'title', 'content']
    template_name = 'messaging/message_new.html'

    def get(self, request, *args, **kwargs):
        context = {}
        context['messageForm'] = MessageForm()

        user = get_object_or_404(CustomUser, username=self.request.user)
        context['unread_messages_count'] = Message.objects.filter(recipients=user).filter(is_read=False).count()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        messageForm = MessageForm(request.POST)
        if messageForm.is_valid():
            sender = get_object_or_404(CustomUser, username=self.request.user)
            recipients = messageForm.cleaned_data['recipients']
            # Create a message for each recipient so that they can archive messages independently.
            for recipient in recipients:
                message = Message.objects.create(
                    sender = sender,
                    title = messageForm.cleaned_data['title'],
                    content = messageForm.cleaned_data['content']
                )
                message.recipients.add(recipient)
            return redirect('messaging:messages-sent')
        context = {'messageForm': MessageForm()}
        return render(request, self.template_name, context)

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
        return render(request, 'messaging/message_new.html', context)

class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message

    # Delete message
    def post(self, request, pk, *args, **kwargs):
        message = get_object_or_404(Message, pk=pk)
        message.delete()
        return redirect('messaging:messages-received')

class MessageArchiveView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'messaging/messages_archived.html'

    # Set message archived for current user
    def post(self, request, pk, *args, **kwargs):
        message = get_object_or_404(Message, pk=pk)
        message.is_archived = True
        message.save()
        return redirect('messaging:messages-archived')

class MessageArchivedListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'messaging/messages_archived.html'
    context_object_name = 'messaging'
    paginate_by = 5

    def get_queryset(self):
        archived_messages = Message.objects.filter(recipients=self.request.user, is_archived=True).order_by('-date_posted')
        return archived_messages

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(CustomUser, username=self.request.user)
        context['unread_messages_count'] = Message.objects.filter(recipients=user).filter(is_read=False).count()
        return context

def search(request):
    if request.is_ajax():
        query = request.GET.get("term", "")
        # Search for a users with search term
        try:
            users = CustomUser.objects.filter(
                        ~Q(username=request.user.username) &
                        Q(username__istartswith=query) |
                        Q(first_name__istartswith=query) |
                        Q(last_name__istartswith=query)
                    ).order_by('username')
        except error:
            messages.add_message(request, messages.ERROR, error)
    return HttpResponse(get_recipient_list(users), 'application/json')

def get_recipient_list(users):
    result = []

    # Add users to result list
    for user in users:
        option = { 'id': user.id, 'label': user.first_name + ' ' +  user.last_name + ' (' + user.username + ')' }
        result.append(option)

    return json.dumps(result)
