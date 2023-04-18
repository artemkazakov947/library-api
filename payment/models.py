from django.db import models
from enumchoicefield import ChoiceEnum, EnumChoiceField

from borrowing.models import Borrowing


class StatusEnum(ChoiceEnum):
    PENDING = "pending"
    PAID = "paid"


class TypeEnum(ChoiceEnum):
    PAYMENT = "payment"
    FINE = "fine"


class Payment(models.Model):
    status = EnumChoiceField(StatusEnum)
    type = EnumChoiceField(TypeEnum)
    borrowing = models.OneToOneField(Borrowing, on_delete=models.CASCADE, related_name="payment")
    session_url = models.URLField(max_length=255)
    session_id = models.TextField()

    @property
    def money_to_pay(self):
        delta = self.borrowing.expected_return_date - self.borrowing.borrow_date
        return delta.days * self.borrowing.book.daily_fee
