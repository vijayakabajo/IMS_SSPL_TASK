from django.db import models

# Create your models here.
class Purchase(models.Model):
    purchase_number = models.IntegerField(blank=False, null=False)
    supplier_name = models.CharField(max_length=100, null=False, blank=False)
    
