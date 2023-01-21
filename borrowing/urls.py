from django.urls import path

from borrowing.views import BorrowingListView, BorrowingDetailView

urlpatterns = [
    path("borrowings/", BorrowingListView.as_view(), name="list-borrowing"),
    path("borrowings/<int:pk>/", BorrowingDetailView.as_view(), name="detail-borrowing"),
]

app_name = "borrowings"
