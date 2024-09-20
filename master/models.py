from django.db import models
from django.core.validators import RegexValidator

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    contact_number = models.CharField(
        max_length=10,
        validators=[RegexValidator(r'^\d{10}$', 'Enter a 10-digit mobile number')]#Note:Unique: True (will add later)
    )
    status = models.SmallIntegerField(default=1)                #pseudo delete

    def __str__(self):
        return self.name      #returns name instead of object

class Item(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)    #100.00
    status = models.SmallIntegerField(default=1)   #pseudo delete