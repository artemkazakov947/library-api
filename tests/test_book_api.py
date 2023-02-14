from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from book_service.models import Book
from book_service.serializers import BookSerializer

BOOK_URL = reverse("book_service:list_create-book")


def book_detail_page(book_id):
    return reverse("book_service:detail-book", args=[book_id])


def book_sample(**params):
    default = {
        "title": "Test book_",
        "author": "Test author_",
        "cover": "Hard",
        "inventory": 10,
        "daily_fee": 1,
    }
    default.update(params)
    return Book.objects.create(**default)


class UnauthenticatedBookTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_list_book_allowed(self):
        resp = self.client.get(BOOK_URL)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_detail_book_authenticated_required(self):
        resp = self.client.get(book_detail_page(1))

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedBookTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test_user@test.com", password="test12345"
        )
        self.client.force_authenticate(self.user)
        for book in range(10):
            book_sample(
                title=f"Test book_{book}",
                author=f"Test author_{book}",
                cover="Hard",
                inventory=book,
                daily_fee=book,
            )

    def test_list_book(self):
        resp = self.client.get(BOOK_URL)

        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, serializer.data)

    def test_detail_book_page_allowed(self):
        book = Book.objects.get(id=2)
        resp = self.client.get(book_detail_page(book.id))

        serializer = BookSerializer(book)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data, serializer.data)

    def test_post_book_forbidden(self):
        payload = {
            "title": "Test book",
            "author": "Test author",
            "cover": "Hard",
            "inventory": 10,
            "daily_fee": 1,
        }

        resp = self.client.post(BOOK_URL, payload)

        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_book_delete_forbidden(self):
        book = Book.objects.get(id=1)
        url = book_detail_page(book.id)
        resp = self.client.delete(url)

        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_book_patch_forbidden(self):
        payload = {"title": "New title"}

        book = Book.objects.get(id=1)
        url = book_detail_page(book.id)
        resp = self.client.patch(url, payload)

        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)


class AdminBookTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

        self.admin = get_user_model().objects.create_superuser(
            email="admin@admin.com", password="user12345", is_staff=True
        )
        self.client.force_authenticate(self.admin)

    def test_create_book_allowed(self):
        payload = {
            "title": "Test book",
            "author": "Test author",
            "cover": "Hard",
            "inventory": 10,
            "daily_fee": 1,
        }
        resp = self.client.post(BOOK_URL, payload)
        book = Book.objects.get(id=resp.data["id"])

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data["title"], book.title)

    def test_patch_book_allowed(self):
        book_sample()
        payload = {"title": "New Title"}
        book = Book.objects.get(id=1)
        url = book_detail_page(book.id)

        resp = self.client.patch(url, payload)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["title"], payload["title"])

    def test_delete_book_allowed(self):
        book_sample()
        book = Book.objects.get(pk=1)

        url = book_detail_page(book.id)

        resp = self.client.delete(url)

        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
