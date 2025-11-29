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
