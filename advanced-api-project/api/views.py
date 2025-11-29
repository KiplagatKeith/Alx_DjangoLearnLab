from django.shortcuts import render
from rest_framework import generics
from .serializers import BookSerializer, AuthorSerializer
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
        if serializer.instance.author.user != self.request.user:
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
        if instance.author.user != self.request.user:
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
        # automatically set the author as the logged-in user
        author = Author.objects.get(user=self.request.user)
        serializer.save(author=author)
