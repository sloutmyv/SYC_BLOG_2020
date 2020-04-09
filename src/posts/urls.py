from django.contrib import admin
from django.urls import path
from .views import (
    posts_create,
    posts_delete,
    posts_update,
    PostListView,
    PostDetailView,
    )

app_name = 'posts'

urlpatterns = [
    path('',PostListView.as_view(), name='posts-list'),
    path('<slug:slug>/',PostDetailView.as_view(), name='post-detail'),
    path('create/', posts_create),
    path('update/', posts_update),
    path('delete/', posts_delete),
]
