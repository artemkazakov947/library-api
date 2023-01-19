from rest_framework import generics

from book_service.models import Book
from book_service.permissions import IsAdminOrIsAuthenticatedOrAnonReadOnly, IsAdminOrIsAuthenticatedReadOnly
from book_service.serializers import BookSerializer


class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAdminOrIsAuthenticatedOrAnonReadOnly, )


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAdminOrIsAuthenticatedReadOnly, )
