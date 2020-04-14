from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse
from django.utils import timezone
from taggit.models import Tag


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

class PostDetailView(DetailView):
    template_name = "posts/post_detail.html"
    model = Post


    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.draft or self.object.publish > timezone.now().date():
            if self.request.user != self.object.user:
                raise Http404
        return context

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
            queryset = super().get_queryset().filter(user__username__iexact=str(author))
        elif private_space is not None and str(private_space) == str(self.request.user):
            queryset = Post.objects.ofuser(str(private_space))
        elif tag is not None:
            queryset = super().get_queryset().filter(tags__name__iexact=tag)
        else:
            queryset = super().get_queryset()

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

class TagsView(TemplateView):
    template_name = "posts/tags_page.html"

    def get_context_data(self, *args, **kwargs):
        context = super(TagsView, self).get_context_data(*args, **kwargs)
        context['tags'] = Tag.objects.all().order_by('name')
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
