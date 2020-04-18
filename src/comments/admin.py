from django.contrib import admin
from .models import Comment

class CommentAdmin(admin.ModelAdmin):
    list_display = ["user","parent_id","id"]
    # list_filter = ["updated"]
    # search_fields = ["title", "content"]
    class Meta:
        model = Comment

admin.site.register(Comment, CommentAdmin)
