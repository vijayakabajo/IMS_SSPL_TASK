from django.shortcuts import render, redirect
from .models import Supplier, Item
from .forms import SupplierForm, ItemForm


#Homepage
def homepage(request):
    return render(request, 'homepage.html')

# Supplier page
def supplier_page(request):
    suppliers = Supplier.objects.filter(status=True)
    return render(request, 'supplier_page.html', {'suppliers': suppliers})

# Item page
def items_page(request):
    items = Item.objects.filter(status=True)
    return render(request, 'items_page.html', {'items': items})

# Add supplier
def add_supplier(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('supplier_page')   #redirecting after adding supplier
    else:
        form = SupplierForm()
    return render(request, 'add_supplier.html', {'form': form})

# Edit supplier
def edit_supplier(request, supplier_id):
    supplier = Supplier.objects.get(id=supplier_id)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect('supplier_page')
    else:
        form = SupplierForm(instance=supplier)
    return render(request, 'edit_supplier.html', {'form': form})

# Delete supplier
def delete_supplier(request, supplier_id):
    supplier = Supplier.objects.get(id=supplier_id)
    supplier.status = False      #softdlt
    supplier.save()
    return redirect('supplier_page')

# Add item
def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('items_page')
    else:
        form = ItemForm()
    return render(request, 'add_item.html', {'form': form})


# Edit item
def edit_item(request, item_id):
    item = Item.objects.get(id=item_id)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('items_page')
    else:
        form = ItemForm(instance=item)
    return render(request, 'edit_item.html', {'form': form})

# Delete item (soft delete)
def delete_item(request, item_id):
    item = Item.objects.get(id=item_id)
    item.status = False #softdel
    item.save()
    return redirect('items_page')

