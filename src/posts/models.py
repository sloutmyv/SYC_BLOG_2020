from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=120)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)         # everytime
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)           # initialy

    def __str__(self):                                                          # python 3
        return self.title
