from django.urls import path
from .views import list_books, LibraryDetailView, register_view, login_view, logout_view

urlpatterns = [
    # Function-based view: list all books
    path('books/', list_books, name='all_books'),

    # Class-based view: details for a specific library
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),

     # Authentication URLs
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]