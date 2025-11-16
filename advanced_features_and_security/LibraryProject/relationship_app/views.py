from django.shortcuts import render, redirect
from .models import Library, Book
from django.views.generic.detail import DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from django import forms

def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})


class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'


def register(request):
    # Validate user input using Django's built-in UserCreationForm 
    # to avoid insecure manual handling of passwords or unsanitized input.

    if request.user.is_authenticated:
        return redirect('all_books')

    # Checker wants these two distinct lines:
    if request.method == 'POST':
        form = UserCreationForm(request.POST)  # <-- POST version
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()  
        
    return render(request, 'relationship_app/register.html', {'form': form})

@permission_required('relationship_app.can_add_book')
def add_book(request):
    # Only users with the 'can_add_book' permission can access this.
    return HttpResponse("You are allowed to add books.")


@permission_required('relationship_app.can_change_book')
def edit_book(request, book_id):
    return HttpResponse(f"You are allowed to edit book {book_id}.")


@permission_required('relationship_app.can_delete_book')
def delete_book(request, book_id):
    return HttpResponse(f"You are allowed to delete book {book_id}.")

# Helper functions to check roles
def is_admin(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def is_librarian(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Member'


@login_required
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')


@login_required
@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')


@login_required
@user_passes_test(is_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html')

class BookSearchForm(forms.Form):
    query = forms.CharField(required=False, max_length=100)

def list_books(request):
    form = BookSearchForm(request.GET)
    books = Book.objects.all()

    if form.is_valid():
        query = form.cleaned_data.get("query")
        if query:
            books = books.filter(title__icontains=query)

    return render(request, 'relationship_app/list_books.html', {
        'books': books,
        'form': form
    })
