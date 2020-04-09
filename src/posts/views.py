from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic import DetailView, ListView, CreateView, UpdateView

from .forms import PostModelForm
from .models import Post


class PostCreateView(CreateView):
    template_name = "posts/post_create.html"
    form_class = PostModelForm

class PostDetailView(DetailView):
    template_name = "posts/post_detail.html"
    model = Post

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        return context

class PostListView(ListView):
    template_name = "posts/posts_list.html"
    model = Post
    paginate_by = 10

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        return context

class PostUpdateView(UpdateView):
    template_name = "posts/post_create.html"
    form_class = PostModelForm

    def get_object(self):
        slug_ = self.kwargs.get("slug")
        return get_object_or_404(Post, slug=slug_)

def posts_delete(request):
    return HttpResponse("<h1>delete</h1>")
