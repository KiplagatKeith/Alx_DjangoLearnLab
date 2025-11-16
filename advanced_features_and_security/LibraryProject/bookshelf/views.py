from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from .models import Book
from django import forms
from django.db.models import Q
from .forms import ExampleForm
@permission_required('bookshelf.can_create', raise_exception=True)
def book_search(request):
    query = request.GET.get('q', '')  # Get user input from query string
    if query:
        # Safe ORM filtering
        books = Book.objects.filter(title__icontains=query)
    else:
        books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})


# Form to validate search input
class SearchForm(forms.Form):
    query = forms.CharField(required=False, max_length=100)

@permission_required('bookshelf.can_create', raise_exception=True)
def book_list(request):
    form = SearchForm(request.GET)
    books = Book.objects.all()

    # Secure handling of user input
    if form.is_valid():
        query = form.cleaned_data.get("query")
        if query:
            books = books.filter(title__icontains=query)  # safe ORM filtering

    return render(request, 'bookshelf/book_list.html', {
        'books': books,
        'form': form,
    })
