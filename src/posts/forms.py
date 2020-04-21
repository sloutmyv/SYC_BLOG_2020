from django import forms
# from pagedown.widgets import PagedownWidget
from .models import Post

class PostModelForm(forms.ModelForm):
    # content = forms.CharField(widget=PagedownWidget)
    publish = forms.DateField(help_text='au format YYYY-MM-DD')
    class Meta:
        model = Post
        fields = [
            'title',
            'tags',
            'content',
            'draft',
            'publish',
        ]
