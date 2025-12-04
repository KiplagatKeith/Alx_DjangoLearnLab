from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Post

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