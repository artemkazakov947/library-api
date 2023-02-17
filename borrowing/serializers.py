import os

from django.db import transaction
from rest_framework import serializers

from book_service.models import Book
from book_service.serializers import BookSerializer
from borrowing.models import Borrowing, get_return_date
from borrowing.telegram_notification import borrowing_telegram_notification


class BorrowingListSerializer(serializers.ModelSerializer):
    book_title = serializers.SlugRelatedField(
        source="book", slug_field="title", many=False, read_only=True
    )

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "book_title",
            "user",
        )


class BorrowingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
        )
        read_only_fields = ("borrow_date",)

    def validate(self, attrs):
        if "expected_return_date" not in attrs:
            attrs["expected_return_date"] = get_return_date()
        data = super(BorrowingCreateSerializer, self).validate(attrs)
        Borrowing.validate_dates(
            attrs["expected_return_date"],
            attrs["actual_return_date"],
            serializers.ValidationError,
        )
        book_id = data["book"].id
        book = Book.objects.get(pk=book_id)
        if book.inventory < 1:
            raise serializers.ValidationError(
                ({"book": f"We have not currently {book}"})
            )

        return data

    def create(self, validated_data):
        with transaction.atomic():
            book = validated_data["book"]
            book.inventory -= 1
            book.save()
            borrowing = Borrowing.objects.create(**validated_data)
            message = (
                f"New borrowing! "
                f" Book: id {book.id}. Title:'{book.title}' by {book.author}."
                f" Borrowing date: {borrowing.borrow_date.strftime('%d/%m/%Y')}."
                f" Expecting return: {borrowing.expected_return_date.strftime('%d/%m/%Y')}."
                f" Borrower_id: {borrowing.user.id}."
            )
            borrowing_telegram_notification(
                message, os.getenv("CHAT_ID"), os.getenv("BOT_TOKEN")
            )
        return borrowing


class BorrowingDetailSerializer(serializers.ModelSerializer):
    book = BookSerializer(many=False, read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
        )
