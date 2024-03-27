from rest_framework import serializers
from advertisement.serializers import AdvertisementSerializer
from booking.models import Booking

class BookingSerializer(serializers.ModelSerializer):
  advertisement_info = AdvertisementSerializer(source='advertisement', read_only=True)
  class Meta:
    model = Booking
    fields = '__all__'
    extra_kwargs = {'advertisement': {'write_only': True}}

  def validate(self, data):
    if data["check_in_date"] > data["check_out_date"]:
      raise serializers.ValidationError({
          "check_out_date": "Check-out date cannot be before than Check-in date.",
      })
    return super(BookingSerializer, self).validate(data)