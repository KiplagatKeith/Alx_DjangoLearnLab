from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Post, Comment, Tag

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
    # Use a CharField to allow new tags as comma-separated values
    tags = forms.CharField(
        required=False,
        help_text="Enter tags separated by commas (e.g., Django, Python, Tutorial)"
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pre-fill tags for existing post
        if self.instance.pk:
            self.fields['tags'].initial = ', '.join([tag.name for tag in self.instance.tags.all()])

    def save(self, commit=True):
        # Save the Post instance first
        post = super().save(commit=False)

        if commit:
            post.save()

        # Handle tags
        tags_str = self.cleaned_data['tags']
        tag_names = [t.strip() for t in tags_str.split(',') if t.strip()]
        # Clear existing tags
        post.tags.clear()
        for name in tag_names:
            tag, created = Tag.objects.get_or_create(name=name)
            post.tags.add(tag)

        return post


class CommentForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your comment here...'}),
        max_length=1000,
        help_text="Maximum 1000 characters."
    )

    class Meta:
        model = Comment
        fields = ['content']