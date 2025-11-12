from django.db import models

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length = 200)
    author = models.CharField(max_length = 100)
    publication_year = models.IntegerField()

    class Meta:
        permissions = [
            ("can_create", "Can create a new book"),
            ("can_delete", "Can delete a book"),
        ]
        
    def __str__(self):
        return f"Title: {self.title}, Author: {self.author}, Publication date: {self.publication_year}"
