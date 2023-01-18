from django.db import models
from djmoney.models.fields import MoneyField


class Book(models.Model):

    class CoverChoices(models.TextChoices):
        HARD = "Hard"
        SOFT = "Soft"

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover = models.CharField(max_length=4, choices=CoverChoices.choices, default="Hard")
    inventory = models.IntegerField()
    daily_fee = MoneyField(max_digits=4, decimal_places=2, default_currency="USD")

    def __str__(self) -> str:
        return f"'{self.title}' by {self.author}"
