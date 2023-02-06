from datetime import date

from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from borrowing.models import Borrowing
from borrowing.serializers import (
    BorrowingListSerializer,
    BorrowingDetailSerializer,
    BorrowingCreateSerializer,
)


class BorrowingViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = BorrowingListSerializer
    queryset = Borrowing.objects.all().select_related("book")
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        responses={status.HTTP_200_OK: BorrowingDetailSerializer},
    )
    @action(
        methods=["GET"],
        detail=True,
        url_path="return",
        permission_classes=[IsAuthenticated],
    )
    def borrowing_return_view(self, request, pk=None):
        """By this action user makes return of book with certain id along with it this book inventory increases by 1"""
        borrowing = Borrowing.objects.get(id=self.kwargs["pk"])
        if borrowing.actual_return_date is not None:
            raise ValidationError("This borrowing has been already returned!")
        borrowing.actual_return_date = date.today()
        book = borrowing.book_id
        book.inventory += 1
        book.save()
        borrowing.save()
        serializer = BorrowingDetailSerializer(borrowing, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowingListSerializer
        if self.action == "create":
            return BorrowingCreateSerializer
        if self.action in ["retrieve", "return"]:
            return BorrowingDetailSerializer

    def get_queryset(self) -> QuerySet:
        queryset = self.queryset
        is_active = self.request.GET.get("is_active")
        user = self.request.GET.get("user")
        if self.request.user.is_staff is True:
            if is_active:
                if user == "":
                    return queryset.exclude(actual_return_date__isnull=False)
                return queryset.filter(user_id=int(user)).exclude(
                    actual_return_date__isnull=False
                )
            return queryset
        if is_active:
            return queryset.filter(user=self.request.user).exclude(
                actual_return_date__isnull=False
            )
        return queryset.filter(user=self.request.user)

    def perform_create(self, serializer) -> None:
        serializer.save(user=self.request.user)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="user",
                type={"type": "int"},
                description="Filter for admins. "
                "Use along with parameter is_active "
                "(ex ?user_id&is_active=true will return borrowings of all users. "
                "?user_id=1&is_active=true will return borrowing of user with id 1)",
                required=False,
            ),
            OpenApiParameter(
                name="is_active",
                description="Filter by actual_return_date (ex ?is_active=true) only for authenticated non admin users",
                required=False,
                allow_blank=True,
            ),
        ],
    )
    def list(self, request, *args, **kwargs):
        return super(BorrowingViewSet, self).list(request, *args, **kwargs)
