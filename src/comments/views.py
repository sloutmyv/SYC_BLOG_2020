from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from django.views.generic import DeleteView

from .models import Comment

class CommentDeleteView(LoginRequiredMixin, DeleteView):
    login_url = '/permissiondenied/'
    template_name = "comments/comment_delete.html"

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Comment, id=id_)

    def get_success_url(self):
        return reverse('posts:posts-list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        #print(self.object.children())
        if self.object.user == request.user:
            success_url = self.get_success_url()
            if self.object.is_parent:
                for child in self.object.children():
                    child.delete()
            self.object.delete()
            return HttpResponseRedirect(success_url)
        else:
            return HttpResponseForbidden("Cannot delete other's comments")

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['id'] = self.kwargs.get("id")
        context['slug'] = self.kwargs.get("slug")
        return context
