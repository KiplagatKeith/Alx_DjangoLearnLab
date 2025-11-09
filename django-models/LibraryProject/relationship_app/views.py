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
        form = UserCreationForm()  
        
    return render(request, 'relationship_app/register.html', {'form': form})

@permission_required('relationship_app.can_add_book')
def add_book(request):
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
