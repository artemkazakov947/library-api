import os
from datetime import date, timedelta
from borrowing.models import Borrowing
from borrowing.telegram_notification import borrowing_telegram_notification


def last_day_borrowing():
    return date.today() + timedelta(days=1)


def get_overdue_borrowing() -> [Borrowing]:
    overdue_query = Borrowing.objects.filter(
        expected_return_date__lte=last_day_borrowing()
    )
    if len(overdue_query) == 0:
        borrowing_telegram_notification(
            "No borrowings overdue today!", os.getenv("CHAT_ID"), os.getenv("BOT_TOKEN")
        )
    return overdue_query


def overdue_notification(overdue_query: [Borrowing]) -> None:
    for borrowing in overdue_query:
        if borrowing.actual_return_date is None:
            days_overdue = last_day_borrowing() - borrowing.expected_return_date
            message = (
                f" Overdue borrowing!"
                f" Book: id {borrowing.book.id}. Title:'{borrowing.book.title}' by {borrowing.book.author}."
                f" Borrowing date: {borrowing.borrow_date.strftime('%d/%m/%Y')}."
                f" Overdue: {days_overdue.days} days"
                f" Borrower_id: {borrowing.user.id}."
            )
            borrowing_telegram_notification(
                message, os.getenv("CHAT_ID"), os.getenv("BOT_TOKEN")
            )
