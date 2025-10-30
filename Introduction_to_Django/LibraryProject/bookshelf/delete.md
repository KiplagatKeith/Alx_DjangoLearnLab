Command:

# Fetch and delete the updated book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()

# Confirm deletion by retrieving all remaining books
Book.objects.all()


Expected Output:

(1, {'bookshelf.Book': 1})
<QuerySet []>


Explanation:
The book record was successfully deleted from the database.
The empty QuerySet [] confirms that there are no remaining entries with that title.
