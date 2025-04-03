from django import forms
from ckeditor.fields import RichTextField
from .models import Post, Comment

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'short_desc', 'content', 'image']
        widgets = {
            'content': RichTextField()
        }


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
