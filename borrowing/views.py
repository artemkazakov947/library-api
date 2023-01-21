from rest_framework import generics

from borrowing.models import Borrowing
from borrowing.serializers import BorrowingListSerializer


class BorrowingListView(generics.ListAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingListSerializer

