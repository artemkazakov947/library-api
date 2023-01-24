from rest_framework import serializers

from book_service.models import Book
from book_service.serializers import BookSerializer
from borrowing.models import Borrowing


class BorrowingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book_id",
            "user_id",
        )


class BorrowingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book_id",
            "user_id",
        )
        read_only_fields = ("borrow_date",)

    def validate(self, attrs):
        data = super(BorrowingCreateSerializer, self).validate(attrs)
        Borrowing.validate_dates(
            attrs["expected_return_date"],
            attrs["actual_return_date"],
            serializers.ValidationError,
        )
        book_id = data["book_id"].id
        book = Book.objects.get(pk=book_id)
        if book.inventory < 1:
            raise serializers.ValidationError(
                ({"book_id": f"We have not currently {book}"})
            )

        return data

    def create(self, validated_data):
        return Borrowing.objects.create(**validated_data)


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
