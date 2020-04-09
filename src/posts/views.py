from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic import DetailView
from .models import Post

def posts_create(request):
    return HttpResponse("<h1>Create</h1>")

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

def posts_update(request):
    return HttpResponse("<h1>update</h1>")

def posts_delete(request):
    return HttpResponse("<h1>delete</h1>")
