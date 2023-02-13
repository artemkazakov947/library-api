from datetime import timedelta, date

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from book_service.models import Book


def get_return_date():
    return date.today() + timedelta(days=14)


class Borrowing(models.Model):
    borrow_date = models.DateField(default=date.today)
    expected_return_date = models.DateField(blank=True, default=get_return_date)
    actual_return_date = models.DateField(blank=True, null=True)
    book = models.ForeignKey(Book, related_name="borrowings", on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="borrowings"
    )

    @staticmethod
    def validate_dates(expected_return: date, actual_return: date, error) -> None:
        if expected_return < date.today():
            raise error({"expected_return_date": "Invalid date - renewal in past!"})
        if get_return_date() < expected_return:
            raise error(
                {
                    "expected_return_date": "Enter a date between now and 2 weeks (default 2)."
                }
            )
        if actual_return and actual_return < date.today():
            raise error({"actual_return_date": "Invalid date - renewal in past!"})

    def clean(self) -> None:
        Borrowing.validate_dates(
            self.expected_return_date, self.actual_return_date, ValidationError
        )

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.full_clean()
        return super(Borrowing, self).save(
            force_insert, force_update, using, update_fields
        )

    def __str__(self) -> str:
        return f"{self.book.title} borrowed by {self.user}"
