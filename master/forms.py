from django import forms
from .models import Supplier, Item

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'contact_number', 'address']

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'price', 'image']

        widgets = {
            'price': forms.NumberInput(attrs={
                'min': '0',  # Set the minimum value to 0
                'step': '100.0'  # Optional: allows decimal values
            }),
        }


        #validatin
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price < 0:
            raise forms.ValidationError("Price cannot be negative.")
        return price
    

