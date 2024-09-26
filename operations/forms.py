# forms.py
from django import forms
from .models import TempTable, PurchaseMaster
from master.models import Supplier, Item

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

class PurchaseMasterForm(forms.ModelForm):
    class Meta:
        model = PurchaseMaster
        fields = ['supplier_id']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['supplier_id'].queryset = Supplier.objects.filter(status=1)
        self.fields['supplier_id'].label = "Supplier"
