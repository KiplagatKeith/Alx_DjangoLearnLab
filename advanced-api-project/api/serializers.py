from rest_framework import serializers
from .models import Book, Author

# Serializer for Book model 
class BookSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    # Custom validation for publication_date field
    def validate_publication_date(self, value):
        if value.year < 1450:
            raise serializers.ValidationError("Publication date cannot be before the invention of the printing press.")
        return value
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_date']

# Serializer for Author model having nested BookSerializer
class AuthorSerializer(serializers.ModelSerializer):
    book = serializers.BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['name', 'book']
