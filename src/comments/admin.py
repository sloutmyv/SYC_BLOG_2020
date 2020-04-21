from django.contrib import admin
from .models import Comment

class CommentAdmin(admin.ModelAdmin):
    list_display = ["user","timestamp","content_type"]
    ordering=['-timestamp']

    class Meta:
        model = Comment

admin.site.register(Comment, CommentAdmin)
