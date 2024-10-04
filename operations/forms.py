# forms.py
from django import forms
from .models import TempTable, PurchaseMaster, SalesMaster, SalesTempTable, SalesDetail, PurchaseDetail
from master.models import Supplier, Item
from django.core.exceptions import ValidationError
from django.db.models import Sum


class PurchaseMasterForm(forms.ModelForm):
    class Meta:
        model = PurchaseMaster
        fields = ['supplier_id']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['supplier_id'].queryset = Supplier.objects.filter(status=1)
        self.fields['supplier_id'].label = "Supplier"

class TempTableForm(forms.ModelForm):
    class Meta:
        model = TempTable
        fields = ['item_id', 'quantity']

        widgets = {
            'quantity': forms.NumberInput(attrs={
                'min': '0',
                'step': '1.0' 
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['item_id'].queryset = Item.objects.filter(status=1)
        self.fields['item_id'].label = "Item"
        self.fields['quantity'].label = "Quantity"

    def clean_item_id(self):
        item_id = self.cleaned_data.get('item_id')
        if TempTable.objects.filter(item_id=item_id).exists():
            raise forms.ValidationError("Item already exists in the List.")
        return item_id
    
    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity <= 0:
            raise forms.ValidationError("Quantity must be greater than 0.")
        return quantity
    


# ------------------------------------------------Sales forrm------------------------------------------------



class SalesMasterForm(forms.ModelForm):
    class Meta:
        model = SalesMaster
        fields = ['seller', 'bill_date']
        widgets = {
            'bill_date': forms.DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['seller'].queryset = Supplier.objects.filter(status=1)
        self.fields['seller'].label = "Seller"



class SalesTempForm(forms.ModelForm):
    class Meta:
        model = SalesTempTable
        fields = ['item', 'quantity']

        widgets = {
            'quantity': forms.NumberInput(attrs={
                'min': '0',
                'step': '1.0' 
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['item'].queryset = Item.objects.filter(status=1)
        self.fields['item'].label = "Item"
        self.fields['quantity'].label = "Quantity"

    def clean_item(self):
        item = self.cleaned_data.get('item')
        if SalesTempTable.objects.filter(item=item).exists():
            raise forms.ValidationError("Item already exists in the List.")
        return item

    def clean_quantity(self):
        # Check if there are already errors in the 'item' field, skip further validation
        if self.errors.get('item'):
            return self.cleaned_data.get('quantity')

        quantity = self.cleaned_data.get('quantity')
        item = self.cleaned_data.get('item')

        if quantity <= 0:
            raise forms.ValidationError("Quantity must be greater than 0.")

        # Calculate the available stock
        total_purchased = PurchaseDetail.objects.filter(item_id_id=item).aggregate(total=Sum('quantity'))['total'] or 0
        total_sold = SalesDetail.objects.filter(item_id=item).aggregate(total=Sum('quantity'))['total'] or 0
        available_stock = total_purchased - total_sold

        # Validate that the quantity does not exceed available stock
        if quantity > available_stock:
            raise ValidationError(f"The quantity cannot exceed the available stock.")

        return quantity


