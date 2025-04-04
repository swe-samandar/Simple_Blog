from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Post, Comment

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'categories', 'short_desc', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'categories': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'short_desc': forms.TextInput(attrs={'class': 'form-control'}),
            'content': CKEditorWidget(),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
