from django.db import models

# Create your models here.
class Purchase(models.Model):
    purchase_number = models.IntegerField(blank=False, null=False, unique=True)
    supplier_name = models.CharField(max_length=100, null=False, blank=False)
    item_name = models.CharField(max_length=100, null=False, blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False )
    total = models.DecimalField(max_digits=10, decimal_places=)