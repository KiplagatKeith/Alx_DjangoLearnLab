from django.urls import path
from .views import list_books, LibraryDetailView

urlpatterns = [
    # Function-based view: list all books
    path('books/', list_books, name='all_books'),

    # Class-based view: details for a specific library
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
]
