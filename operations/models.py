from django.db import models

# Create your models here.
class PurchaseMaster(models.Model):
    invoice_number = models.IntegerField(blank=False, null=False, unique=True)
    supplier_id = models.CharField(max_length=100, null=False, blank=False)
    status = models.SmallIntegerField(default=1, null=False)
    total = models.DecimalField(max_digits=10, decimal_places=2)

class PurchaseDetail(models.Model):
    item_name = models.CharField(max_length=100, null=False, blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False )
    quantity = models.IntegerField(null=False, blank=False)
    status = models.SmallIntegerField(default=1, null=False)
    status = models.SmallIntegerField(default=1, null=False)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    