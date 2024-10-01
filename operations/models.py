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
    
#-------------------------------------------Sales Models-------------------------------------------------
 

class SalesMaster(models.Model):
    seller = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    bill_number = models.CharField(max_length=20, null=False, blank=False)
    bill_date = models.DateField(blank=False, null=False)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateField(auto_now_add=True)
    status = models.SmallIntegerField(default=1, null=False)

    def save(self, *args, **kwargs):
        if not self.bill_number:
            last_bill = SalesMaster.objects.order_by('bill_number').last()
            if last_bill and last_bill.bill_number.startswith('BILL-'):
                last_bill_num = int(last_bill.bill_number.split('-')[1])
                new_bill_num = last_bill_num + 1
            else:
                new_bill_num = 1000
            self.bill_number = f"BILL-{new_bill_num}"
        super(SalesMaster, self).save(*args, **kwargs)   
   
    def __str__(self):
        return f"{self.bill_number} - {self.seller}"

class SalesDetail(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False)
    items_total = models.DecimalField(max_digits=10, decimal_places=2)
    sales_master = models.ForeignKey(SalesMaster, on_delete=models.CASCADE, related_name='sales_details')
    created_at = models.DateTimeField(auto_now_add=True) 
    status = models.SmallIntegerField(default=1, null=False)
    
    def __str__(self):
        return f"{self.item} - {self.quantity}"

class SalesTempTable(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False)
    items_total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(default=1, null=False)

    def __str__(self):
        return f"{self.item} - {self.quantity}"

    