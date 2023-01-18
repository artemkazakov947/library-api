from django.db import models
from djmoney.models.fields import MoneyField


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover = models.TextChoices("cover", "HARD SOFT")
    inventory = models.IntegerField()
    daily_fee = MoneyField(max_digits=4, decimal_places=2, default_currency="USD")

    def __str__(self) -> str:
        return f"Book {Book.title} by {Book.author}"
