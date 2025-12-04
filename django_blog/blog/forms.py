from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Post, Comment

# Registration form
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

# User info form for profile editing
class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]

# Profile info form for bio and profile picture
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["bio", "profile_pic"]

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content"]

class CommentForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your comment here...'}),
        max_length=1000,
        help_text="Maximum 1000 characters."
    )

    class Meta:
        model = Comment
        fields = ['content']