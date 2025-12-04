from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register_view, profile_view, home_view, posts_view

urlpatterns = [
    path("", home_view, name="home"),
    path("posts/", posts_view, name="posts"),

    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(template_name="logout.html"), name="logout"),
    path("register/", register_view, name="register"),
    path("profile/", profile_view, name="profile"),
]
