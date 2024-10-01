from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from .models import PurchaseMaster, PurchaseDetail, TempTable, SalesDetail, SalesTempTable, SalesMaster, SalesMaster, SalesDetail, SalesTempTable, Supplier
from master.models import Supplier, Item
from .forms import TempTableForm, PurchaseMasterForm, SalesMasterForm , SalesTempForm, SalesMasterForm, SalesTempForm
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Sum




#-----------------------------------------------------purchase page--------------------------------------------------------


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



#-------------------------------------------------------Sales view------------------------------------------------




def sales_page(request):
    seller_id = request.session.get('seller_id', None)
    seller_name = request.session.get('seller_name', '')
    seller_contact = request.session.get('seller_contact', '')
    # Retain the date in the session
    bill_date = request.session.get('bill_date', None)

    if seller_id:
        initial_data = {'seller': seller_id, 'bill_date': bill_date}  # Retaining the date
    else:
        initial_data = {'bill_date': bill_date}

    temp_items = SalesTempTable.objects.all().order_by('-created_at')  # Fetch temp table data
    sales_form = SalesMasterForm(initial=initial_data)
    temp_form = SalesTempForm()

    if request.method == 'POST':
        # Add item to temp table
        if 'add_item' in request.POST:
            temp_form = SalesTempForm(request.POST)
            if temp_form.is_valid():
                temp_item = temp_form.save(commit=False)
                temp_item.items_total = temp_item.item.price * temp_item.quantity
                temp_item.save()

                # Retain seller and bill date in the session
                seller_id = request.POST.get('seller')
                bill_date = request.POST.get('bill_date')
                
                seller = Supplier.objects.get(id=seller_id)
                request.session['seller_id'] = seller_id
                request.session['seller_name'] = seller.name
                request.session['seller_contact'] = seller.contact_number
                request.session['bill_date'] = bill_date  # Storing the date

                return redirect('sales-create')

        # Finalize sales
        if 'finalize_sales' in request.POST:
            # Check if temp table is empty before processing the sale
            if not temp_items.exists():
                messages.error(request, "Add items to the sales list before finalizing.")
            else:
                sales_form = SalesMasterForm(request.POST)
                if sales_form.is_valid():  # Validate only SalesMasterForm
                    with transaction.atomic():
                        sales_master = sales_form.save(commit=False)
                        # Calculate subtotal
                        sales_master.sub_total = sum(item.items_total for item in temp_items)
                        sales_master.save()

                        # Move items from SalesTempTable to SalesDetail
                        for temp_item in temp_items:
                            SalesDetail.objects.create(
                                sales_master=sales_master,
                                item=temp_item.item,
                                quantity=temp_item.quantity,
                                items_total=temp_item.items_total
                            )

                        # Clear the SalesTempTable after sale
                        SalesTempTable.objects.all().delete()

                        # Clear the seller data and date from the session
                        request.session.pop('seller_id', None)
                        request.session.pop('seller_name', None)
                        request.session.pop('seller_contact', None)
                        request.session.pop('bill_date', None)

                    return redirect('sales_master_list')

    sub_total = sum(item.items_total for item in temp_items)

    # Generate new bill number
    last_bill = SalesMaster.objects.order_by('bill_number').last()
    if last_bill and last_bill.bill_number.startswith('BILL-'):
        last_bill_num = int(last_bill.bill_number.split('-')[1])
        bill_number = f"BILL-{last_bill_num + 1}"
    else:
        new_bill_num = 1000
        bill_number = f"BILL-{new_bill_num}"

    context = {
        'sales_form': sales_form,
        'temp_form': temp_form,
        'temp_items': temp_items,
        'sub_total': sub_total,
        'bill_number': bill_number,
        'seller_name': seller_name,
        'seller_contact': seller_contact,
    }
    return render(request, 'sales.html', context)





#remove item from temp table

def remove_item_sales_temp(request, item_id):
    if request.method == 'POST':
        try:
            temp_item = SalesTempTable.objects.get(id=item_id)
            temp_item.delete()

            # Calculate the updated subtotal
            temp_items = SalesTempTable.objects.all() 
            sub_total = sum(item.items_total for item in temp_items)

            # Return a JSON response with success and the updated subtotal
            return JsonResponse({'success': True, 'sub_total': float(sub_total)})

        except TempTable.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Item not found.'})

    return JsonResponse({'success': False, 'error': 'Invalid request.'})




# Sales Master Page
def sales_master_list(request):
    sales = SalesMaster.objects.all().order_by('-bill_number')
    return render(request, 'sales_master_list.html', {'sales': sales})

# Sales Detail Page
def sales_detail_view(request, pk):
    # Fetch the specific SalesMaster by its primary key
    sales_master = get_object_or_404(SalesMaster, pk=pk)
    # Fetch all SalesDetails associated with the SalesMaster
    sales_details = SalesDetail.objects.filter(sales_master=sales_master)
    return render(request, 'sales_detail_view.html', {'sales_master': sales_master, 'sales_details': sales_details})

def get_available_stock(request, item_id):
    
    if item_id:
        # Total quantity purchased
        total_purchased = PurchaseDetail.objects.filter(item_id_id=item_id).aggregate(
            total=Sum('quantity')  # Use Sum to aggregate the quantity field
        )['total'] or 0
        
        # Total quantity sold
        total_sold = SalesDetail.objects.filter(item_id=item_id).aggregate(
            total=Sum('quantity')  # Use Sum to aggregate the quantity field
        )['total'] or 0
        
        # Available stock is purchased - sold
        available_stock = total_purchased - total_sold

        return JsonResponse({'available_stock': available_stock})
    
    return JsonResponse({'error': 'Item not found'}, status=400)