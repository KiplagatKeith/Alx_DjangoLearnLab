from django.urls import path
from relationship_app.views import all_books_view, LibraryDetailView

urlpatterns = [
    # Function-based view: list all books
    path('books/', all_books_view, name='all_books'),

    # Class-based view: details for a specific library
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
]
