from django.contrib import admin
from django.urls import path
from .views import (
    posts_delete,
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    )

app_name = 'posts'

urlpatterns = [
    path('',PostListView.as_view(), name='posts-list'),
    path('article/<slug:slug>/',PostDetailView.as_view(), name='post-detail'),
    path('create/', PostCreateView.as_view(), name='post-create'),
    path('article/<slug:slug>/update/', PostUpdateView.as_view(), name='post-update'),
    path('delete/', posts_delete),
]
