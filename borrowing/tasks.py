from celery import shared_task

from borrowing.overdue_notification import overdue_notification, get_overdue_borrowing


@shared_task
def daily_task() -> None:
    overdue_notification(get_overdue_borrowing())
