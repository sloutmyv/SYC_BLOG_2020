from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import pre_save                                   # pour la création des signaux
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe
from .utils import unique_slug_generator      # Slug generator
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager

from comments.models import Comment

# Modifying Post.objects.all()
class PostManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now())

    def ofuser(self, auteur, *args, **kwargs):
        return super(PostManager, self).filter(user__username__iexact=auteur)

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE,verbose_name="Auteur")
    title = models.CharField(max_length=120,verbose_name="Article(s)")
    slug  = models.SlugField(null=True, blank=True, editable=False, verbose_name="Slug") #necesite une instance title.
    content = RichTextUploadingField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True,verbose_name="Écrit le")         # everytime
    updated = models.DateTimeField(auto_now=True, auto_now_add=False,verbose_name="Mise à jour le")           # initialy
    tags = TaggableManager(blank=True)

    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False, auto_now_add=False,verbose_name="Publié le")

    objects = PostManager() # could call it another way but Post.objets.all()

    def __str__(self):                                                          # python 3
        return self.title

    def get_absolute_url(self):
        return reverse("posts:post-detail", kwargs={"slug": self.slug})

    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type



### Signals de création des slugs
def rl_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug=unique_slug_generator(instance)

pre_save.connect(rl_pre_save_receiver, sender=Post)
