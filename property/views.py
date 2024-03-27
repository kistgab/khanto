from rest_framework import viewsets, permissions
from property.models import Property
from property.serializers import PropertySerializer


# Create your views here.
class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = PropertySerializer
