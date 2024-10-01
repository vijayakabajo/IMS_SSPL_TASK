# forms.py
from django import forms
from .models import TempTable, PurchaseMaster, SalesMaster, SalesTempTable
from master.models import Supplier, Item


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
        quantity = self.cleaned_data.get('quantity')
        if quantity <= 0:
            raise forms.ValidationError("Quantity must be greater than 0.")
        return quantity

