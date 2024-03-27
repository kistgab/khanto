from django.db import models

# Create your models here.


class Property(models.Model):
    max_guests = models.SmallIntegerField()
    bathroom_count = models.SmallIntegerField()
    accept_pets = models.BooleanField()
    cleaning_fee = models.DecimalField(max_digits=10, decimal_places=2)
    activation_date = models.DateField()
    creation_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
