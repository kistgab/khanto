from django.db import models

from advertisement.models import Advertisement

# Create your models here.
class Booking(models.Model):
  advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE)
  check_in_date = models.DateField()
  check_out_date = models.DateField()
  total_value = models.DecimalField(max_digits=10, decimal_places=2)
  comments = models.TextField()
  total_guests = models.SmallIntegerField()
  creation_date = models.DateTimeField(auto_now_add=True)
  last_updated = models.DateTimeField(auto_now=True)