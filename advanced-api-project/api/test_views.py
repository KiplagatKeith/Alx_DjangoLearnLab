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

    # ----------------- LIST & DETAIL -----------------
    def test_list_books(self):
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_book_detail(self):
        url = reverse('book-detail', kwargs={'id': self.book1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)

    def test_book_detail_not_found(self):
        url = reverse('book-detail', kwargs={'id': 999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # ----------------- CREATE -----------------
    def test_create_book_authenticated(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('book-create')
        data = {
            "title": "New Book",
            "publication_year": 2023
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], "New Book")
        self.assertEqual(response.data['author'], self.author1.id)

    def test_create_book_unauthenticated(self):
        url = reverse('book-create')
        data = {"title": "New Book", "publication_year": 2023}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # ----------------- UPDATE -----------------
    def test_update_book_author(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('book-update', kwargs={'id': self.book1.id})
        data = {"title": "Updated Title", "publication_year": 2020}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Title")

    def test_update_book_non_author_forbidden(self):
        self.client.force_authenticate(user=self.user2)
        url = reverse('book-update', kwargs={'id': self.book1.id})
        data = {"title": "Hacked Title", "publication_year": 2020}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ----------------- DELETE -----------------
    def test_delete_book_author(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('book-delete', kwargs={'id': self.book1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book1.id).exists())

    def test_delete_book_non_author_forbidden(self):
        self.client.force_authenticate(user=self.user2)
        url = reverse('book-delete', kwargs={'id': self.book1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Book.objects.filter(id=self.book1.id).exists())

    # ----------------- FILTER, SEARCH, ORDER -----------------
    def test_filter_books_by_title(self):
        url = reverse('book-list') + "?title=Book One"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Book One")

    def test_search_books_by_author_name(self):
        url = reverse('book-list') + "?search=Author One"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_order_books_by_publication_year(self):
        url = reverse('book-list') + "?ordering=-publication_year"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, sorted(years, reverse=True))
