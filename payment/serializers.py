from rest_framework import serializers

from borrowing.serializers import BorrowingDetailSerializer
from payment.models import Payment


class PaymentBaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = "__all__"

    def get_money_to_pay(self, obj):
        return obj.money_to_pay

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["money_to_pay"] = str(ret["money_to_pay"])
        return ret


class PaymentListSerializer(PaymentBaseSerializer):
    user_id = serializers.SlugRelatedField(source="borrowing.user", slug_field="id", many=False, read_only=True)
    book = serializers.SlugRelatedField(source="borrowing.book", slug_field="title", many=False, read_only=True)

    class Meta:
        model = Payment

        fields = ("id", "user_id", "book", "borrowing", "status", "type", "money_to_pay")


class PaymentDetailSerializer(PaymentBaseSerializer):
    borrowing = BorrowingDetailSerializer(many=False, read_only=True)

    class Meta:
        model = Payment
        fields = ("id", "status", "type", "borrowing", "session_url", "session_id", "money_to_pay")
