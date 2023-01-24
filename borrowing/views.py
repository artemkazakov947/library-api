from rest_framework import generics

from borrowing.models import Borrowing
from borrowing.serializers import (
    BorrowingListSerializer,
    BorrowingDetailSerializer,
    BorrowingCreateSerializer,
)


class BorrowingListView(generics.ListCreateAPIView):
    serializer_class = BorrowingListSerializer

    def get_serializer_class(self):
        if self.request.method == "GET":
            return BorrowingListSerializer
        return BorrowingCreateSerializer

    def get_queryset(self):
        queryset = Borrowing.objects.all()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(user_id=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)


class BorrowingDetailView(generics.RetrieveAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingDetailSerializer
