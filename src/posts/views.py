from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import FormMixin
from django.views.generic.list import ListView
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse
from django.utils import timezone
from taggit.models import Tag

from comments.form import CommentForm
from comments.models import Comment
from .forms import PostModelForm
from .models import Post

class PostCreateView(LoginRequiredMixin, CreateView):
    login_url = '/permissiondenied/'
    template_name = "posts/post_create.html"

    form_class = PostModelForm
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        form.save_m2m()
        return HttpResponseRedirect(obj.get_absolute_url())

class PostDetailView(FormMixin, DetailView):
    template_name = "posts/post_detail.html"
    model = Post
    form_class = CommentForm


    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.draft or self.object.publish > timezone.now().date():
            if self.request.user != self.object.user:
                raise Http404
        context['comments'] = self.object.comments

        initial_data = {
                        "user": self.request.user,
                        "content_type": self.object.get_content_type,
                        "object_id": self.object.id}
        context['form'] = self.form_class(initial=initial_data)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            obj = form.save(commit=False)
            try:
                parent_id = int(request.POST.get("parent_id"))
            except:
                parent_id = None
            if parent_id:
                parent_qs = Comment.objects.filter(id=parent_id)
                if parent_qs.exists() and parent_qs.count()==1:
                     obj.parent = parent_qs.first()
            obj.save()
            return HttpResponseRedirect(self.object.get_absolute_url())
        else:
            return self.form_invalid(form)

class PostListView(ListView):
    template_name = "posts/posts_list.html"
    model = Post
    queryset = Post.objects.active()


    ordering = ['-timestamp']
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get("q")
        author = self.kwargs.get('author')
        private_space = self.kwargs.get('privatespace')
        tag = self.kwargs.get('tag_url')

        if query:
            queryset = super().get_queryset().filter(
                        Q(title__icontains=query)|
                        Q(content__icontains=query)
                        ).distinct()
        elif author is not None:
            queryset = super().get_queryset().filter(user__username__iexact=str(author)).order_by('-publish')
        elif private_space is not None and str(private_space) == str(self.request.user):
            queryset = Post.objects.ofuser(str(private_space)).order_by('-publish')
        elif tag is not None:
            queryset = super().get_queryset().filter(tags__name__iexact=tag).order_by('-publish')
        else:
            queryset = super().get_queryset().order_by('-publish')

        return queryset


    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['nb_post_published'] = self.get_queryset().count()
        return context

class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/permissiondenied/'
    template_name = "posts/post_create.html"
    form_class = PostModelForm

    def get_object(self):
        slug_ = self.kwargs.get("slug")
        return get_object_or_404(Post, slug=slug_)

class PostDeleteView(LoginRequiredMixin, DeleteView):
    login_url = '/permissiondenied/'
    template_name = "posts/post_delete.html"

    def get_object(self):
        slug_ = self.kwargs.get("slug")
        return get_object_or_404(Post, slug=slug_)

    def get_success_url(self):
        return reverse('posts:posts-list')

    # override the delete function to check for a user match
    def delete(self, request, *args, **kwargs):
        # the Post object
        self.object = self.get_object()
        if self.object.user == request.user:
            success_url = self.get_success_url()
            self.object.delete()
            return HttpResponseRedirect(success_url)
        else:
            return HttpResponseForbidden("Cannot delete other's posts")

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['slug'] = self.kwargs.get("slug")
        return context

class TagsView(TemplateView):
    template_name = "posts/tags_page.html"

    def get_context_data(self, *args, **kwargs):
        context = super(TagsView, self).get_context_data(*args, **kwargs)
        context['tags'] = Tag.objects.all().exclude(name__iexact="draft").order_by('name')
        all_tags =Tag.objects.all().values()
        liste_lettres = []
        for i in all_tags:
            if i['name'][0] not in liste_lettres:
                liste_lettres.append(i['name'][0])
            else:
                pass
        context['lettres'] = sorted(liste_lettres)
        context['common_tags'] = Post.tags.most_common()[:10]
        return context
