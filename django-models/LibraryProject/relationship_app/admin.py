from django.contrib import admin
from relationship_app.models import Author, Book, Library, Librarian

# -------------------------
# Author admin
# -------------------------
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# -------------------------
# Book admin
# -------------------------
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')
    list_filter = ('author',)
    search_fields = ('title', 'author__name')

# -------------------------
# Library admin
# -------------------------
@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    filter_horizontal = ('books',)  # nice dual-select widget for ManyToMany

# -------------------------
# Librarian admin
# -------------------------
@admin.register(Librarian)
class LibrarianAdmin(admin.ModelAdmin):
    list_display = ('name', 'library')
    search_fields = ('name', 'library__name')
