from rest_framework import serializers

from book_service.serializers import BookSerializer
from borrowing.models import Borrowing


class BorrowingListSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source="book_id.title", read_only=True)
    book_author = serializers.CharField(source="book_id.author", read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book_title",
            "book_author",
            "user_id",
        )


class BorrowingDetailSerializer(serializers.ModelSerializer):
    book = BookSerializer(source="book_id", many=False, read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user_id",
        )
