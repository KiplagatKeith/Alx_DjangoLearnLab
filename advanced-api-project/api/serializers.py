from rest_framework import serializers
from .models import Book, Author

# Serializer for Book model
class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    - Represents the book's title, author (as string), and publication year.
    """

    #author = serializers.StringRelatedField()
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    
    def validate_publication_year(self, value):
        if value > 2024:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']  # match your model

# Serializer for Author model with nested books
class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model.
    - Includes a nested list of books associated with the author.
    - 'books' uses BookSerializer for read-only representation.
    """
    
    books = BookSerializer(many=True, read_only=True)  # use the class name directly

    class Meta:
        model = Author
        fields = ['name', 'books']
