from django.db import models

class Author(models.Model):
    name = models.CharField(max_length = 100)

    def __str__(self):
        return f"Name: {self.name}"
    
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(
        Author, 
        on_delete=models.CASCADE,
        related_name='books'
    )

    def __str__(self):
        return f"Title: {self.title}, Author: {self.author}"
    
class Library(models.Model):
    name = models.CharField(max_length=255)
    books = models.ManyToManyField(
        Book,
        related_name='libraries'
    )

class Librarian(models.Model):
    name = models.CharField(max_length=255)
    library = models.OneToOneField(
        Library,
        on_delete=models.CASCADE,
        related_name= 'laibu'
    )

    def __str__(self):
        return f"Name: {self.name}, Library: {self.library}"