from django.contrib import admin
from django.urls import path, re_path
from .views import (
    CommentDeleteView,
    )

app_name = 'comments'

urlpatterns = [
    path('comment/<int:id>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
]
