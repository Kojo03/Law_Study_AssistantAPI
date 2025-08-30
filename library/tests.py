from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Book, LibraryUser, BookCheckout
from datetime import date

User = get_user_model()

class LibraryTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.library_user = LibraryUser.objects.create(
            user=self.user, username='testuser', email='test@example.com'
        )
        self.book = Book.objects.create(
            title='Test Book', author='Test Author', isbn='1234567890123',
            published_date=date.today(), copies_available=2
        )

    def test_book_creation(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/library/books/', {
            'title': 'New Book', 'author': 'New Author', 'isbn': '9876543210987',
            'published_date': '2023-01-01', 'copies_available': 5
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_book_checkout(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/library/checkout/', {'book_id': self.book.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.book.refresh_from_db()
        self.assertEqual(self.book.copies_available, 1)

    def test_book_return(self):
        self.client.force_authenticate(user=self.user)
        # First checkout
        checkout_response = self.client.post('/library/checkout/', {'book_id': self.book.id})
        checkout_id = checkout_response.data['id']
        
        # Then return
        return_response = self.client.post('/library/return/', {'checkout_id': checkout_id})
        self.assertEqual(return_response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.copies_available, 2)