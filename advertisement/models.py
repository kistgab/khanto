from django.db import models
from property.models import Property

# Create your models here.

class Advertisement(models.Model):
  property = models.ForeignKey(Property, on_delete=models.CASCADE)
  platform_name = models.CharField(max_length=100)
  platform_fee = models.DecimalField(max_digits=5, decimal_places=2)
  creation_date = models.DateTimeField(auto_now_add=True)
  last_updated = models.DateTimeField(auto_now=True)