# API Documentation: Book Management

## Base URL


## Endpoints


## Endpoints

### 1. List all books
- **URL:** `/books/`
- **Method:** GET
- **Auth:** Not required
- **Query Params:** `?search=<title_or_author_name>`
- **Description:** Returns a searchable list of all books.

### 2. Retrieve a book
- **URL:** `/books/<id>/`
- **Method:** GET
- **Auth:** Not required
- **Description:** Returns the details of a single book by ID.

### 3. Create a book
- **URL:** `/books/create/`
- **Method:** POST
- **Auth:** Required (must be logged in)
- **Description:** Creates a new book. The logged-in user is automatically set as the author.
- **Body Example:**
```json
{
    "title": "My New Book",
    "publication_year": 2025
}
4. Update a book
URL: /books/<id>/update/

Method: PUT/PATCH

Auth: Required

Permissions: Only the author can update

Body Example:

json
Copy code
{
    "title": "Updated Book Title",
    "publication_year": 2026
}
5. Delete a book
URL: /books/<id>/delete/

Method: DELETE

Auth: Required

Permissions: Only the author can delete

Filtering, Searching, and Ordering in BookListView

The BookListView has been enhanced with filtering, searching, and ordering using Django REST Framework and django-filter. These features allow API users to efficiently query the Book database with flexible options.

Enabled Features

Filtering

Searching

Ordering

Below is a detailed explanation of how each feature works, along with example API requests.

1. Filtering

Filtering allows users to retrieve books that match exact field values.

Enabled fields:

title

author__name

publication_year

Use it like this:

GET /api/books/?title=The Hobbit


Multiple filters at once:

GET /api/books/?author__name=Tolkien&publication_year=1937

2. Searching

Searching allows partial text matching using the ?search= parameter.

Enabled search fields:

title

author__name

Examples:

GET /api/books/?search=harry

GET /api/books/?search=rowling


Search is case-insensitive and matches substrings.

3. Ordering

Users can sort results by title or publication year.

Enabled ordering fields:

title

publication_year

Examples:

Sort by title (A → Z)
GET /api/books/?ordering=title

Sort by title (Z → A)
GET /api/books/?ordering=-title

Sort by publication year (oldest → newest)
GET /api/books/?ordering=publication_year

Sort by publication year (newest → oldest)
GET /api/books/?ordering=-publication_year

 Final View Code (for reference)
class BookListView(generics.ListAPIView):
    """
    GET /api/books/

    Supports:
    - Filtering: ?title=..., ?publication_year=..., ?author__name=...
    - Searching: ?search=keyword
    - Ordering: ?ordering=title, ?ordering=-publication_year
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = ['title', 'author__name', 'publication_year']
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']
