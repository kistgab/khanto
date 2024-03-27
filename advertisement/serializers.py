from rest_framework import serializers
from advertisement.models import Advertisement
from property.models import Property
from property.serializers import PropertySerializer

class AdvertisementSerializer(serializers.ModelSerializer):
  property_info = PropertySerializer(source='property', read_only=True)
  class Meta:
    model = Advertisement
    fields = '__all__'