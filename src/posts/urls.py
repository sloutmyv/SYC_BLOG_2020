from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    )

app_name = 'posts'

urlpatterns = [
    path('',PostListView.as_view(), name='posts-list'),
    path('article/<slug:slug>/',PostDetailView.as_view(), name='post-detail'),
    path('create/', PostCreateView.as_view(), name='post-create'),
    path('article/<slug:slug>/update/', PostUpdateView.as_view(), name='post-update'),
    path('article/<slug:slug>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('permissiondenied/', TemplateView.as_view(template_name="permissiondenied.html"), name="permission-denied"),
]
