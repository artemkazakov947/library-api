from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from payment.models import Payment
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
