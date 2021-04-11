from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from django.urls import reverse
from django.views import generic

from .forms import PollForm
from .models import Choice, Question

from project.decorators import unacthenticated_user, allowed_user_types

class IndexView(generic.ListView):
    template_name = 'index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

class ManagePollsView(generic.ListView):
    template_name = 'manage_polls.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')

@allowed_user_types(allowed_roles=['Teacher', 'Admin'])
def add_poll(request):
    if request.method == 'GET':
        pollForm = PollForm()
        return render(request, "add_poll.html", {'pollForm' : pollForm, 'choices': [1,2,3] }) # Note! hardcoded 3 choices
    if request.method == 'POST':
        pollForm = PollForm(request.POST)
        if pollForm.is_valid():
            question = Question()
            question.question_text = pollForm.cleaned_data['question_text']
            question.save()
            question_id = question.id

            for key, value in request.POST.items():
                if key.startswith('choice'):
                    choice_id = key.split('choice')[1]
                    choice = Choice()
                    choice.question_id = question_id
                    choice.choice_text = value
                    choice.save()

            messages.success(request,"Successfully added poll")
            return HttpResponseRedirect(reverse("polls:manage_polls"))
        else:
            messages.error(request,"Failed to add Poll")
            return HttpResponseRedirect(reverse("polls:add_poll"))

@allowed_user_types(allowed_roles=['Teacher', 'Admin'])
def edit_poll(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    choices = Choice.objects.filter(question=question_id)
    if request.method == 'GET':
        return render(request, 'edit_poll.html', {'question': question, 'choices': choices })
    if request.method == 'POST':
        pollForm = PollForm(request.POST)
        if pollForm.is_valid():
            question.question_text = pollForm.cleaned_data['question_text']
            question.save()

            for key, value in request.POST.items():
                if key.startswith('choice'):
                    choice_id = key.split('choice')[1]
                    #print ("%s %s" % (choice_id, value))
                    choice = get_object_or_404(Choice, pk=choice_id)
                    choice.choice_text = value
                    choice.save()
            
            messages.success(request,"Successfully edited poll")
            return HttpResponseRedirect(reverse("polls:edit_poll", kwargs={"question_id":question_id}))
        else:
            messages.error(request,"Failed to edit Poll")
            return HttpResponseRedirect(reverse("polls:edit_poll", kwargs={"question_id":question_id}))

@allowed_user_types(allowed_roles=['Teacher', 'Admin'])
def delete_poll(request, question_id):
    if request.method == 'GET':
        question=Question.objects.get(id=question_id)
        question.delete()
        messages.success(request,"Successfully deleted poll")
        return HttpResponseRedirect(reverse("polls:manage_polls"))
