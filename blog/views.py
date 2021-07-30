from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.views import generic
from django.urls import reverse


class PostList(generic.ListView):

    # The template name defaults to <app name>/<model name (lower case)_list.html
    #template_name = 'blog/post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(
            published_date__lte=timezone.now()).order_by('-published_date')


class PostDetail(generic.DetailView):

    model = Post
    # The template name defaults to <app name>/<model name (lower case)_detail.html
    #template_name = 'blog/post_detail.html'


class PostNew(generic.FormView):

    template_name = 'blog/post_edit.html'
    form_class = PostForm

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.published_date = timezone.now()
        post.save()
        return redirect('post_detail', pk=post.pk)


class PostEdit(generic.UpdateView):

    template_name = 'blog/post_edit.html'
    model = Post
    fields = ['title', 'text']

    def get_success_url(self):
        return reverse('post_edit', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        if form.has_changed():
            post = form.save(commit=False)
            post.author = self.request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)

        return super().form_valid(form)
