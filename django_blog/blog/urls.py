from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    register_view,
    profile_view,
    home_view,
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    add_comment,
    CommentUpdateView,
    CommentDeleteView,
)

urlpatterns = [
    # Home
    path("", home_view, name="home"),

    # Authentication
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(template_name="logout.html"), name="logout"),
    path("register/", register_view, name="register"),
    path("profile/", profile_view, name="profile"),

    # Blog CRUD
    path("posts/", PostListView.as_view(), name="posts"),
    path("posts/new/", PostCreateView.as_view(), name="post_create"),
    path("posts/<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path("posts/<int:pk>/edit/", PostUpdateView.as_view(), name="post_update"),
    path("posts/<int:pk>/delete/", PostDeleteView.as_view(), name="post_delete"),

    # Comment URLs
    path("posts/<int:post_id>/comments/new/", add_comment, name="add_comment"),
    path("comments/<int:pk>/edit/", CommentUpdateView.as_view(), name="comment_update"),
    path("comments/<int:pk>/delete/", CommentDeleteView.as_view(), name="comment_delete"),
]
