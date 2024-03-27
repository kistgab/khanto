from booking.models import Booking
from booking.serializers import BookingSerializer
from rest_framework import viewsets, mixins, permissions


class BookingViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Booking.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = BookingSerializer
