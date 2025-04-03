from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)


    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Profile
        fields = ['user', 'bio', 'email', 'avatar']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['email'].initial = user.email

    def save(self, commit=True):
        profile = super().save(commit=False)
        profile.user.email = self.cleaned_data['email']
        profile.user.save()
        if commit:
            profile.save()
        return profile


from blog.models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'message']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name*'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email*'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Message*', 'rows': 5}),
        }