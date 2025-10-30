# Retrieve all Book records
Book.objects.all()

# Expected Output:
<QuerySet [<Book: Title: 1984, Author: George Orwell, Publication date: 1949>]>

# Retrieve a specific Book record
Book.objects.get(title=1984)

# Expected Output:
<Book: Title: 1984, Author: George Orwell, Publication date: 1949>

# Explanation:
- The first command retrieves all the book records from the database.
- The second command retrieves the specific book with the title 1984.

