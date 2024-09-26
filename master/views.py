from django.shortcuts import render, redirect, get_object_or_404
from .models import Supplier, Item
from .forms import SupplierForm, ItemForm

# Homepage
def homepage(request):
    return render(request, 'homepage.html')

# Supplier Page
def supplier_page(request):
    suppliers = Supplier.objects.filter(status=1)
    return render(request, 'supplier_page.html', {'suppliers': suppliers})

# Item Page
def items_page(request):
    items = Item.objects.filter(status=1).order_by('-created_At')
    return render(request, 'items_page.html', {'items': items})

# Handle Supplier
def handle_supplier(request, action, supplier_id=None):
    if action == 'add':
        if request.method == 'POST':
            form = SupplierForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('supplier_page')
        else:
            form = SupplierForm()
        return render(request, 'add_supplier.html', {'form': form, 'action': action})

    elif action == 'edit':
        supplier = get_object_or_404(Supplier, id=supplier_id)
        if request.method == 'POST':
            form = SupplierForm(request.POST, instance=supplier)
            if form.is_valid():
                form.save()
                return redirect('supplier_page')
        else:
            form = SupplierForm(instance=supplier)
        return render(request, 'edit_supplier.html', {'form': form, 'action': action})

    elif action == 'delete':
        supplier = get_object_or_404(Supplier, id=supplier_id)
        supplier.status = 0  # Soft delete
        supplier.save()
        return redirect('supplier_page')

# Handle Items
def handle_items(request, action, item_id=None):
    if action == 'add':
        if request.method == 'POST':
            form = ItemForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('items_page')
        else:
            form = ItemForm()
        return render(request, 'add_item.html', {'form': form, 'action': action})

    elif action == 'edit':
        item = get_object_or_404(Item, id=item_id)
        if request.method == 'POST':
            form = ItemForm(request.POST,  request.FILES, instance=item)
            if form.is_valid():
                form.save()
                return redirect('items_page')
        else:
            form = ItemForm(instance=item)
        return render(request, 'edit_item.html', {'form': form, 'action': action, 'item': item })

    elif action == 'delete':
        item = get_object_or_404(Item, id=item_id)
        item.status = 0  # Soft delete
        item.save()
        return redirect('items_page')


# # Add supplier
# def add_supplier(request):
#     if request.method == 'POST':
#         form = SupplierForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('supplier_page')   #redirecting after adding supplier
#     else:
#         form = SupplierForm()
#     return render(request, 'add_supplier.html', {'form': form})

# # Edit supplier
# def edit_supplier(request, supplier_id):
#     supplier = Supplier.objects.get(id=supplier_id)
#     if request.method == 'POST':
#         form = SupplierForm(request.POST, instance=supplier)
#         if form.is_valid():
#             form.save()
#             return redirect('supplier_page')
#     else:
#         form = SupplierForm(instance=supplier)
#     return render(request, 'edit_supplier.html', {'form': form})

# # Delete supplier
# def delete_supplier(request, supplier_id):
#     supplier = Supplier.objects.get(id=supplier_id)
#     supplier.status = False      #softdlt
#     supplier.save()
#     return redirect('supplier_page')





# # Add item
# def add_item(request):
#     if request.method == 'POST':
#         form = ItemForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('items_page')
#     else:
#         form = ItemForm()
#     return render(request, 'add_item.html', {'form': form})


# # Edit item
# def edit_item(request, item_id):
#     item = Item.objects.get(id=item_id)
#     if request.method == 'POST':
#         form = ItemForm(request.POST, instance=item)
#         if form.is_valid():
#             form.save()
#             return redirect('items_page')
#     else:
#         form = ItemForm(instance=item)
#     return render(request, 'edit_item.html', {'form': form})

# # Delete item (soft delete)
# def delete_item(request, item_id):
#     item = Item.objects.get(id=item_id)
#     item.status = False #softdel
#     item.save()
#     return redirect('items_page')


        
        
        
        
        
