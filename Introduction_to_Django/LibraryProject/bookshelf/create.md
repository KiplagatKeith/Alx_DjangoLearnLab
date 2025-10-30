Command:

# Create a Book instance
Book.objects.create(title='1984', author='George Orwell', publication_year=1949)


Expected Output:

<Book: Title: 1984, Author: George Orwell, Publication date: 1949>


Explanation:
A new record was successfully created in the database with the provided title, author, and publication year.
This confirms that the create() method is working properly.
