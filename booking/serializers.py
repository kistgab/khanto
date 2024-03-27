from rest_framework import serializers
from advertisement.serializers import AdvertisementSerializer
from booking.models import Booking


class BookingSerializer(serializers.ModelSerializer):
    advertisement_info = AdvertisementSerializer(source="advertisement", read_only=True)

    class Meta:
        model = Booking
        fields = "__all__"
        extra_kwargs = {"advertisement": {"write_only": True}}

    def validate(self, data):
        if data["check_in_date"] > data["check_out_date"]:
            raise serializers.ValidationError(
                {
                    "check_out_date": "Check-out date cannot be before than Check-in date.",
                }
            )
        max_allowed_guests = data["advertisement"].property.max_guests
        if data["total_guests"] > max_allowed_guests:
            raise serializers.ValidationError(
                {
                    "total_guests": "Total guests cannot be greater than the maximum number of guests allowed ("
                    + str(max_allowed_guests)
                    + ").",
                }
            )
        existing_bookings_in_period = Booking.objects.filter(
            advertisement__property=data["advertisement"].property,
            check_out_date__gte=data["check_in_date"],
            check_in_date__lte=data["check_out_date"],
        )
        if existing_bookings_in_period.exists():
            raise serializers.ValidationError(
            {
                "check_in_date": "There is already a booking in the selected period.",
            }
            )
        return super(BookingSerializer, self).validate(data)
