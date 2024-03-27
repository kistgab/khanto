from advertisement.models import Advertisement
from advertisement.serializers import AdvertisementSerializer
from rest_framework import viewsets, mixins, permissions

class AdvertisementViewSet(mixins.CreateModelMixin,
                           mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.ListModelMixin,
                           viewsets.GenericViewSet
                          ):
  queryset = Advertisement.objects.all()
  permission_classes = [permissions.AllowAny]
  serializer_class = AdvertisementSerializer