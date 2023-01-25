from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from borrowing.models import Borrowing
from borrowing.serializers import (
    BorrowingListSerializer,
    BorrowingDetailSerializer,
    BorrowingCreateSerializer,
)


class BorrowingListView(generics.ListCreateAPIView):
    serializer_class = BorrowingListSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return BorrowingListSerializer
        return BorrowingCreateSerializer

    def get_queryset(self):
        queryset = Borrowing.objects.all()
        is_active = self.request.GET.get("is_active")
        user = self.request.GET.get("user_id")
        if self.request.user.is_staff is True:
            if is_active == "":
                if user == "":
                    return queryset.exclude(actual_return_date__isnull=False)
                elif user != "":
                    return queryset.filter(user_id_id=user).exclude(actual_return_date__isnull=False)
            return queryset
        if is_active == "":
            return queryset.filter(user_id=self.request.user).exclude(actual_return_date__isnull=False)
        return queryset.filter(user_id=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)


class BorrowingDetailView(generics.RetrieveAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingDetailSerializer
