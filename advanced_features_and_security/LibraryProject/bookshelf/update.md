Command:

# Fetch the book instance
book = Book.objects.get(title="1984")

# Update the title
book.title = "Nineteen Eighty-Four"

# Save the changes
book.save()

# Confirm the update
Book.objects.all()


Expected Output:

<QuerySet [<Book: Title: Nineteen Eighty-Four, Author: George Orwell, Publication date: 1949>]>


Explanation:
The book title was updated from “1984” to “Nineteen Eighty-Four”, and the changes were saved to the database successfully.
