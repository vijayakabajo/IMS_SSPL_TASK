from django.db import models
from master.models import Supplier, Item
from django.core.validators import RegexValidator


#-----------------------------------------------Purchase Models----------------------------------------------------------

class PurchaseMaster(models.Model):
    invoice_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    supplier_id = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True) 
    status = models.SmallIntegerField(default=1, null=False)
    

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            last_invoice = PurchaseMaster.objects.order_by('invoice_number').last()
            if last_invoice and last_invoice.invoice_number.startswith('INV-'):
                last_invoice_num = int(last_invoice.invoice_number.split('-')[1])
                new_invoice_num = last_invoice_num + 1
            else:
                new_invoice_num = 1000
            self.invoice_number = f"INV-{new_invoice_num}"
        super(PurchaseMaster, self).save(*args, **kwargs)

    def __str__(self):
        return self.invoice_number


class PurchaseDetail(models.Model):
    purchase_master = models.ForeignKey(PurchaseMaster, on_delete=models.CASCADE, related_name='purchase_details')
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE) 
    quantity = models.IntegerField(null=False, blank=False)
    items_total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True) 
    status = models.SmallIntegerField(default=1, null=False)

    def __str__(self):
        return f"{self.item_id.name} - {self.purchase_master.invoice_number}"


class TempTable(models.Model):
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE, unique=True)
    quantity = models.IntegerField(null=False, blank=False)
    items_total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True) 
    status = models.SmallIntegerField(default=1, null=False)

    def __str__(self):
        return f"{self.item_id.name} - {self.quantity}"
    