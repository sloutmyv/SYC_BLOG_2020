from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'user',
            'content_type',
            'object_id',
            'content',
        ]
        widgets = {
        'user': forms.HiddenInput(),
        'content_type': forms.HiddenInput(),
        'object_id': forms.HiddenInput(),
        }



    # content_type = forms.CharField(widget=forms.HiddenInput)
    # object_id = forms.IntegerField(widget=forms.HiddenInput)
    # #parent_id = forms.IntegerField(widget=forms.HiddenInput, required=False)
    # content = forms.CharField(widget=forms.Textarea)
