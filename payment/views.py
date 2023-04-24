import stripe
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from payment.models import Payment, StatusEnum
from payment.serializers import PaymentListSerializer, PaymentDetailSerializer


class PaymentViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Payment.objects.all().select_related("borrowing")
    
    def get_serializer_class(self):
        serializer_classes = {
            "list": PaymentListSerializer,
            "retrieve": PaymentDetailSerializer
        }
        return serializer_classes[self.action]

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset
        return self.queryset.filter(borrowing__user=self.request.user)

    @action(
        methods=["GET"],
        detail=True,
        permission_classes=[IsAuthenticated],
        url_path="success"
    )
    def payment_success(self, request, pk=None):
        payment = Payment.objects.get(id=self.kwargs["pk"])
        session = stripe.checkout.Session.retrieve(payment.session_id)
        if session.payment_status == "paid":
            payment.status = StatusEnum.PAID
            payment.save()
            return Response({"message": "Payment successful"}, status=status.HTTP_200_OK)

        return Response({"error": "Payment failed"}, status=status.HTTP_200_OK)

    @action(
        methods=["GET"],
        detail=True,
        permission_classes=[IsAuthenticated],
        url_path="cancel"
    )
    def payment_cancel(self, request, pk=None):
        return Response({"message": "Session canceled. You can pay later within 24 hours."})
