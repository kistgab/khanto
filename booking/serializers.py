from rest_framework import serializers
from booking.models import Booking

class BookingSerializer(serializers.ModelSerializer):
  class Meta:
    model = Booking
    fields = '__all__'
    # depth = 1

  def validate(self, data):
    if data["check_in_date"] > data["check_out_date"]:
      raise serializers.ValidationError({
          "check_out_date": "Check-out date cannot be before than Check-in date.",
      })
    return super(BookingSerializer, self).validate(data)