from django.shortcuts import render, get_object_or_404, render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from project.utils import is_staff, is_author
from users.models import CustomUser
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post
from .forms import NewsForm

class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'news/news.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'news/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(CustomUser, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'news/post_form.html'

    def get(self, request, *args, **kwargs):
        context = {}
        context['newsForm'] = NewsForm()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        newsForm = NewsForm(request.POST)
        if newsForm.is_valid():
            user = get_object_or_404(CustomUser, username=self.request.user)
            post = Post.objects.create(
                title = newsForm.cleaned_data['title'],
                content = newsForm.cleaned_data['content'],
                author_id = user.id
            )
            return redirect('news')
        return redirect('post-create')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return is_staff(self)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'news/post_update_form.html'

    def get(self, request, pk, *args, **kwargs):
        post = get_object_or_404(Post, pk=pk)
        data = {
            "title": post.title,
            "content": post.content,
        }
        context = {
            "newsForm": NewsForm(initial=data),
        }
        return render(request, self.template_name, context)

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return is_author(self)

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/news'

    def test_func(self):
        return is_author(self)
