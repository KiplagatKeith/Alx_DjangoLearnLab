from django.shortcuts import render
from rest_framework import generics
from serializers import BookSerializer, AuthorSerializer
from .models import Book
from rest_framework import permissions
from rest_framework import filters
class BookListView(generics.ListAPIView):
    """
    API view to retrieve a list of books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter]  # add filter backends as needed
    search_fields = ['title', 'author']  # example search fields

class BookDetailView(generics.RetrieveAPIView):
    """
    API view to retrieve details of a specific book by its ID.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'id'

class BookUpdateView(generics.UpdateAPIView):
    """
    API view to update details of a specific book by its ID.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticated]  # only logged-in users

    def perform_update(self, serializer):
        # Example: only allow the owner to update the book
        if serializer.instance.owner != self.request.user:
            raise PermissionError("You cannot edit this book.")
        serializer.save()
class BookDeleteView(generics.DestroyAPIView):
    """
    API view to delete a specific book by its ID.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # only logged-in users
    lookup_field = 'id'

    def perform_destroy(self, instance):
        # Example: only allow the owner to delete the book
        if instance.owner != self.request.user:
            raise PermissionError("You cannot delete this book.")
        instance.delete()

class BookCreateView(generics.CreateAPIView):
    """
    API view to create a new book.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # only logged-in users can create

    def perform_create(self, serializer):
        # Add extra logic before saving
        # For example, assign the book to the currently logged-in user
        serializer.save(owner=self.request.user)