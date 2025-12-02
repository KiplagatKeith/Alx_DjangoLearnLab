from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register_view, profile_view

urlpatterns = [

    # LOGIN
    path("login/", 
         auth_views.LoginView.as_view(template_name="login.html"),
         name="login"),

    # LOGOUT
    path("logout/",
         auth_views.LogoutView.as_view(template_name="logout.html"),
         name="logout"),

    # REGISTER
    path("register/", register_view, name="register"),

    # PROFILE
    path("profile/", profile_view, name="profile"),
]
