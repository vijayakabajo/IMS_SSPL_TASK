from django.db import models
from django.core.validators import RegexValidator

class Supplier(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    contact_number = models.CharField(
        max_length=10,
        blank=False, null=False, unique=True,
        validators=[RegexValidator(r'^\d{10}$', 'Enter a 10-digit mobile number')]#Note:Unique: True (will add later)
    )
    status = models.SmallIntegerField(default=1, null=False)               #pseudo delete

    def __str__(self):
        return self.name      #returns name instead of object

class Item(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)    #100.00
    status = models.SmallIntegerField(default=1, null=False)   #pseudo delete









    # null=false can't be null for db
    # blank=false can't be null for forms