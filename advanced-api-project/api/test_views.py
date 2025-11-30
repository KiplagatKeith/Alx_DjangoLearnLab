# api/test_views.py

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Author, Book


class BookAPITestCase(APITestCase):
    def setUp(self):
        # Create users
        self.user1 = User.objects.create_user(username="user1", password="pass1234")
        self.user2 = User.objects.create_user(username="user2", password="pass1234")

        # Create authors
        self.author1 = Author.objects.create(user=self.user1, name="Author One")
        self.author2 = Author.objects.create(user=self.user2, name="Author Two")

        # Create books
        self.book1 = Book.objects.create(title="Book One", publication_year=2020, author=self.author1)
        self.book2 = Book.objects.create(title="Book Two", publication_year=2021, author=self.author2)
        self.book3 = Book.objects.create(title="Another Book", publication_year=2020, author=self.author1)

    def test_list_books(self):
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_create_book_authenticated(self):
        self.client.login(username="user1", password="pass1234")
        url = reverse('book-list')
        data = {"title": "New Book", "publication_year": 2022}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['author'], self.author1.id)
        self.client.logout()

    def test_create_book_unauthenticated(self):
        url = reverse('book-list')
        data = {"title": "New Book", "publication_year": 2022}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_book_author(self):
        self.client.login(username="user1", password="pass1234")
        url = reverse('book-update', kwargs={"id": self.book1.id})
        data = {"title": "Updated Book", "publication_year": 2021}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Updated Book")
        self.client.logout()

    def test_update_book_non_author_forbidden(self):
        self.client.login(username="user2", password="pass1234")
        url = reverse('book-update', kwargs={"id": self.book1.id})
        data = {"title": "Hack Attempt"}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.logout()

    def test_delete_book_author(self):
        self.client.login(username="user1", password="pass1234")
        url = reverse('book-delete', kwargs={"id": self.book1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.client.logout()

    def test_delete_book_non_author_forbidden(self):
        self.client.login(username="user2", password="pass1234")
        url = reverse('book-delete', kwargs={"id": self.book1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.logout()

    def test_filter_books_by_year(self):
        url = reverse('book-list') + "?publication_year=2020"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_search_books_by_title(self):
        url = reverse('book-list') + "?search=Another"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], "Another Book")
