from django.shortcuts import render
from rest_framework import generics
from .serializers import BookSerializer, AuthorSerializer
from .models import Book, Author
from rest_framework import permissions
from rest_framework import filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
class BookListView(generics.ListAPIView):
    """
    GET /api/books/

    Returns a list of all books in the database.
    Features:
    - Supports search by book title or author name using query param ?search=<query>.
    - No authentication required to view the list.
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer

    filter_backends = [
        DjangoFilterBackend, 
        filters.SearchFilter, 
        filters.OrderingFilter
    ]

    filterset_fields = ['title', 'author__name', 'publication_year']
    # searching
    search_fields = ['title', 'author__name']
    # ordering
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']  # default

    filter_backends = [filters.SearchFilter]  # add filter backends as needed
    search_fields = ['title', 'author_name']  # example search fields
    permission_classes = [IsAuthenticatedOrReadOnly]

class BookDetailView(generics.RetrieveAPIView):
    """
    GET /api/books/<id>/

    Retrieves details of a single book by its ID.
    - Publicly accessible (no login required).
    - Returns 404 if the book ID does not exist.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookUpdateView(generics.UpdateAPIView):
    """
    PUT/PATCH /api/books/<id>/update/

    Allows the author of a book (linked to logged-in user) to update book details.
    Custom Behavior:
    - Checks ownership: only the author can update.
    - Returns PermissionError if user is not the owner.
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]  # only logged-in users

    def perform_update(self, serializer):
        if serializer.instance.author.user != self.request.user:
            raise PermissionError("You cannot edit this book.")
        serializer.save()
class BookDeleteView(generics.DestroyAPIView):
    """
    DELETE /api/books/<id>/delete/

    Allows the author of a book to delete it.
    Custom Behavior:
    - Ownership check: only the author can delete.
    - Returns PermissionError if user is not the owner.
    """
    
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # only logged-in users
    lookup_field = 'id'

    def perform_destroy(self, instance):
        if instance.author.user != self.request.user:
            raise PermissionError("You cannot delete this book.")
        instance.delete()

class BookCreateView(generics.CreateAPIView):
    """
    POST /api/books/create/

    Allows authenticated users to create a new book.
    Custom Behavior:
    - Automatically assigns the logged-in user as the book's author.
    - Requires authentication (403 Forbidden if not logged in).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # only logged-in users can create

    def perform_create(self, serializer):
        # automatically set the author as the logged-in user
        author = Author.objects.get(user=self.request.user)
        serializer.save(author=author)
