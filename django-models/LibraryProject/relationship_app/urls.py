from django.urls import path
from .views import list_books, LibraryDetailView, register_view
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    # Function-based view: list all books
    path('books/', list_books, name='all_books'),

    # Class-based view: details for a specific library
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),

    # Registration view (stays custom)
    path('register/', register_view, name='register'),

    # Built-in authentication class-based views
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
]
