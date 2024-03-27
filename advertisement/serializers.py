from rest_framework import serializers
from advertisement.models import Advertisement
from property.serializers import PropertySerializer


class AdvertisementSerializer(serializers.ModelSerializer):
    property_info = PropertySerializer(source="property", read_only=True)

    class Meta:
        model = Advertisement
        extra_kwargs = {"property": {"write_only": True}}
        fields = "__all__"
