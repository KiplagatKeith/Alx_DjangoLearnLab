from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import RegisterForm, ProfileForm, UserProfileForm, PostForm, CommentForm
from django.contrib.auth.models import User
from .models import Post, UserProfile, Comment
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView 
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404


# -----------------------------
# User Authentication & Profile
# -----------------------------

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("profile")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


@login_required
def profile_view(request):
    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == "POST":
        user_form = ProfileForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect("profile")
    else:
        user_form = ProfileForm(instance=user)
        profile_form = UserProfileForm(instance=user_profile)

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
    }
    return render(request, "profile.html", context)


# -----------------------------
# Home & Posts List View
# -----------------------------

def home_view(request):
    return render(request, "home.html")


# Optional legacy view (you can remove if using PostListView)
def posts_view(request):
    posts = Post.objects.all().order_by('-published_date')
    return render(request, "posts.html", {"posts": posts})


# -----------------------------
# Blog Post CRUD Views
# -----------------------------

# List all posts (public)
class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    ordering = ["-published_date"]


# View single post (public)
class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"


# Create new post (login required)
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # redirect to login if not authenticated
    login_url = 'login'


# Update post (login required + author only)
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"
    login_url = 'login'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user


# Delete post (login required + author only)
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("posts")
    login_url = 'login'

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user

# Create a new comment
@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect("post_detail", pk=post.pk)
    else:
        form = CommentForm()
    return render(request, "blog/comment_form.html", {"form": form, "post": post})

# Update an existing comment
class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user

    def get_success_url(self):
        return reverse_lazy("post_detail", kwargs={"pk": self.object.post.pk})

# Delete an existing comment
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "blog/comment_confirm_delete.html"

    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user

    def get_success_url(self):
        return reverse_lazy("post_detail", kwargs={"pk": self.object.post.pk})
