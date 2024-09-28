from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from .models import PurchaseMaster, PurchaseDetail, TempTable
from master.models import Supplier, Item
from .forms import TempTableForm, PurchaseMasterForm
from django.http import JsonResponse
from django.contrib import messages



#------------------------------------------purchase page--------------------------------------------------------


def purchase_page(request):
    supplier_id = request.session.get('supplier_id', None)
    supplier_name = request.session.get('supplier_name', '')
    supplier_contact = request.session.get('supplier_contact', '')

    if supplier_id:
        initial_data = {'supplier_id': supplier_id}
    else:
        initial_data = {}

    temp_items = TempTable.objects.all().order_by('-created_at')  # Fetch temp table data
    purchase_form = PurchaseMasterForm(initial=initial_data)
    temp_form = TempTableForm()

    if request.method == 'POST':
        # Add item to temp table
        if 'add_item' in request.POST:
            temp_form = TempTableForm(request.POST)
            if temp_form.is_valid():
                temp_item = temp_form.save(commit=False)
                temp_item.items_total = temp_item.item_id.price * temp_item.quantity
                temp_item.save()

                # Retain supplier selection and store details in the session
                supplier_id = request.POST.get('supplier_id')
                supplier = Supplier.objects.get(id=supplier_id)
                request.session['supplier_id'] = supplier_id
                request.session['supplier_name'] = supplier.name
                request.session['supplier_contact'] = supplier.contact_number

                return redirect('purchase-page')

        # Finalize purchase
        if 'finalize_purchase' in request.POST:
            # Check if temp table is empty before processing the purchase
            if not temp_items.exists():
                messages.error(request, "Add items to the purchase list before finalizing.")
            else:
                purchase_form = PurchaseMasterForm(request.POST)
                if purchase_form.is_valid():  # Validate only PurchaseMasterForm
                    with transaction.atomic():
                        purchase_master = purchase_form.save(commit=False)
                        # Calculate subtotal
                        purchase_master.sub_total = sum(item.items_total for item in temp_items)
                        purchase_master.save()

                        # Move items from TempTable to PurchaseDetail
                        for temp_item in temp_items:
                            PurchaseDetail.objects.create(
                                purchase_master=purchase_master,
                                item_id=temp_item.item_id,
                                quantity=temp_item.quantity,
                                items_total=temp_item.items_total
                            )

                        # Clear the TempTable after purchase
                        TempTable.objects.all().delete()

                        # Clear the supplier data from the session
                        if 'supplier_id' in request.session:
                            del request.session['supplier_id']
                        if 'supplier_name' in request.session:
                            del request.session['supplier_name']
                        if 'supplier_contact' in request.session:
                            del request.session['supplier_contact']

                    return redirect('purchase_master_list')

    sub_total = sum(item.items_total for item in temp_items)

    # Generate new invoice number
    last_invoice = PurchaseMaster.objects.order_by('invoice_number').last()
    if last_invoice and last_invoice.invoice_number.startswith('INV-'):
        last_invoice_num = int(last_invoice.invoice_number.split('-')[1])
        invoice_number = f"INV-{last_invoice_num + 1}"
    else:
        new_invoice_num = 1000
        invoice_number = f"INV-{new_invoice_num}"

    context = {
        'purchase_form': purchase_form,
        'temp_form': temp_form,
        'temp_items': temp_items,
        'sub_total': sub_total,
        'invoice_number': invoice_number,
        'supplier_name': supplier_name,
        'supplier_contact': supplier_contact,
    }
    return render(request, 'purchase.html', context)




#Purchase Master Page
def purchase_master_list(request):
    purchases = PurchaseMaster.objects.all().order_by('-created_at')
    return render(request, 'purchase_master_list.html', {'purchases': purchases})

#Purchase Detail Page
def purchase_detail_view(request, pk):
    # Fetch the specific PurchaseMaster by its primary key
    purchase_master = get_object_or_404(PurchaseMaster, pk=pk)
    # Fetch all PurchaseDetails associated with the PurchaseMaster
    purchase_details = PurchaseDetail.objects.filter(purchase_master=purchase_master)
    return render(request, 'purchase_detail_view.html', {'purchase_master': purchase_master, 'purchase_details': purchase_details})

# item price
def get_item_price(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    return JsonResponse({'price': item.price})

# supplier details
def get_supplier_details(request, supplier_id):
    supplier = get_object_or_404(Supplier, id=supplier_id)
    return JsonResponse({'supplier_name': supplier.name, 'supplier_contact': supplier.contact_number})

#remove item from temp table
from django.http import JsonResponse

def remove_item(request, item_id):
    if request.method == 'POST':
        try:
            temp_item = TempTable.objects.get(id=item_id)
            temp_item.delete()

            # Calculate the updated subtotal
            temp_items = TempTable.objects.all()  # Filter according to your context
            sub_total = sum(item.items_total for item in temp_items)

            # Return a JSON response with success and the updated subtotal
            return JsonResponse({'success': True, 'sub_total': sub_total})

        except TempTable.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Item not found.'})

    return JsonResponse({'success': False, 'error': 'Invalid request.'})



    #-----------------------------------------------------sales page-------------------------------------------------

def sales_page(request):
    




    context = {

    }    
    return render(request, 'sales.html', context)