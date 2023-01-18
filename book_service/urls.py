from django.urls import path

from book_service.views import BookListCreateView, BookDetailView

urlpatterns = [
    path("books/", BookListCreateView.as_view(), name="list_create-book"),
    path("books/<int:pk>/", BookDetailView.as_view(), name="detail-book")
]

app_name = "book_service"
