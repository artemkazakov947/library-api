from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from book_service.models import Book
from borrowing.models import Borrowing
from tests.test_book_api import book_sample

BORROWING_URL = reverse("borrowing:borrowing-list")


class BorrowingTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="user@user.com", password="user12345"
        )
        self.client.force_authenticate(self.user)

    def test_borrowing_create_return(self):
        book = book_sample()
        initial_inventory = book.inventory
        payload = {
            "book": book.id,
            "actual_return_date": "",
        }

        resp_create_borrowing = self.client.post(BORROWING_URL, payload)
        borrowing = Borrowing.objects.get(id=1)

        self.assertEqual(resp_create_borrowing.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.get(pk=book.id).inventory, initial_inventory - 1)
        self.assertIn(borrowing, self.user.borrowings.all())

        resp_return_borrowing = self.client.get(
            f"http://127.0.0.1:8000/api/borrowings/{borrowing.id}/return/"
        )

        self.assertEqual(resp_return_borrowing.status_code, status.HTTP_200_OK)
        self.assertEqual(Book.objects.get(pk=book.id).inventory, initial_inventory)
