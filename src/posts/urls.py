from django.contrib import admin
from django.urls import path
from .views import (
    posts_list,
    posts_create,
    posts_delete,
    posts_detail,
    posts_update,
    )

urlpatterns = [
    path('create/', posts_create),
    path('detail/', posts_detail),
    path('', posts_list),
    path('update/', posts_update),
    path('delete/', posts_delete),
]
