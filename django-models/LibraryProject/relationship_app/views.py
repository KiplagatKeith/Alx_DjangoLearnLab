from django.shortcuts import render
from django.http import HttpRequest
from relationship_app.models import Book, Library
from django.views.generic import DetailView

def all_books_view(request):
    books = Book.objects.all()

    return render(request, 'relationship_app/all_books.html', {'books': books})

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
