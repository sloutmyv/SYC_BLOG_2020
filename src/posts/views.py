from django.http import HttpResponse
from django.shortcuts import render

def posts_create(request):
    return HttpResponse("<h1>Create</h1>")

def posts_detail(request):
    return HttpResponse("<h1>Detail</h1>")

def posts_list(request):
    return render(request, "base.html", {})

def posts_update(request):
    return HttpResponse("<h1>update</h1>")

def posts_delete(request):
    return HttpResponse("<h1>delete</h1>")
