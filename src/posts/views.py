from django.http import HttpResponse
from django.shortcuts import render

def posts_create(request):
    return HttpResponse("<h1>Create</h1>")

def posts_detail(request):
    context = {
        "title" : "Detail"
    }
    return render(request, "base.html", context)

def posts_list(request):
    context = {
        "title" : "List"
    }
    return render(request, "base.html", context)

def posts_update(request):
    return HttpResponse("<h1>update</h1>")

def posts_delete(request):
    return HttpResponse("<h1>delete</h1>")
