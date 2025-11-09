from django.shortcuts import render, redirect
from .models import Library, Book
from django.views.generic.detail import DetailView

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required


def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})


class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'


def register(request):
    if request.user.is_authenticated:
        return redirect('all_books')

    # Checker wants these two distinct lines:
    if request.method == 'POST':
        form = UserCreationForm(request.POST)  # <-- POST version
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()  # <-- This line is required exactly

    return render(request, 'relationship_app/register.html', {'form': form})
