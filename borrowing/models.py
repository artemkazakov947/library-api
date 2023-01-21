from datetime import timedelta, date

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from book_service.models import Book


def get_return_date():
    return date.today() + timedelta(days=14)


class Borrowing(models.Model):
    borrow_date = models.DateField()
    expected_return_date = models.DateField(default=get_return_date)
    actual_return_date = models.DateField(blank=True, null=True)
    book_id = models.ForeignKey(
        Book, related_name="borrowings", on_delete=models.CASCADE
    )
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="borrowings"
    )

    @staticmethod
    def validate_dates(borrow_date: date, expected_return: date, actual_return: date, error) -> None:
        if borrow_date != date.today():
            raise error(
                {"borrow_date": f"Borrow date must be today({date.today()})!"}
            )
        if expected_return < borrow_date:
            raise error(
                {"expected_return_date": "Invalid date - renewal in past!"}
            )
        if actual_return:
            if actual_return < borrow_date:
                raise error(
                    {"actual_return_date": "Invalid date - renewal in past!"}
                )
        if borrow_date + timedelta(days=14) < expected_return:
            raise error(
                {"expected_return_date": "Enter a date between now and 2 weeks (default 2)."}
            )

    def clean(self) -> None:
        Borrowing.validate_dates(self.borrow_date, self.expected_return_date, self.actual_return_date, ValidationError)

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if not self.borrow_date:
            self.borrow_date = date.today()
        self.full_clean()
        return super(Borrowing, self).save(
            force_insert, force_update, using, update_fields
        )

    def __str__(self) -> str:
        return f"{self.book_id.title} borrowed by {self.user_id}"