from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.posts_create),
    path('detail/', views.posts_detail),
    path('list/', views.posts_list),
    path('update/', views.posts_update),
    path('delete/', views.posts_delete),
]
