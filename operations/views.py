from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from .models import PurchaseMaster, PurchaseDetail, TempTable
from master.models import Supplier, Item
from .forms import TempTableForm, PurchaseMasterForm
from django.http import JsonResponse



#------------------------------------------purchase page--------------------------------------------------------

def purchase_page(request):
    supplier_id = request.session.get('supplier_id', None)   
    if supplier_id:
        initial_data = {'supplier_id': supplier_id}
    else:
        initial_data = {}

    temp_items = TempTable.objects.all().order_by('-created_at')  #temptable data
    purchase_form = PurchaseMasterForm(initial=initial_data)
    temp_form = TempTableForm()

    if request.method == 'POST':
        if 'add_item' in request.POST:
            temp_form = TempTableForm(request.POST)
            if temp_form.is_valid():
                temp_item = temp_form.save(commit=False)
                temp_item.items_total = temp_item.item_id.price * temp_item.quantity
                temp_item.save()
                
                # Retain supplier selection
                supplier_id = request.POST.get('supplier_id')
                request.session['supplier_id'] = supplier_id
                
                return redirect('purchase-page')

        # Finalize
        if 'finalize_purchase' in request.POST:
            purchase_form = PurchaseMasterForm(request.POST)
            if purchase_form.is_valid():  # Validate only PurchaseMasterForm
                with transaction.atomic():
                    purchase_master = purchase_form.save(commit=False)
                    
                    #sub_total
                    purchase_master.sub_total = sum(item.items_total for item in temp_items)
                    purchase_master.save()

                    for temp_item in temp_items:
                        PurchaseDetail.objects.create(
                            purchase_master=purchase_master,
                            item_id=temp_item.item_id,
                            quantity=temp_item.quantity,
                            items_total=temp_item.items_total
                        )

                    TempTable.objects.all().delete()
                    
                    if 'supplier_id' in request.session:
                        del request.session['supplier_id']

                return redirect('purchase-page')

    sub_total = sum(item.items_total for item in temp_items)

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
    } 
    return render(request, 'purchase.html', context)



def purchase_master_list(request):
    purchases = PurchaseMaster.objects.all().order_by('-created_at')
    return render(request, 'purchase_master_list.html', {'purchases': purchases})

def purchase_detail_view(request, pk):
    # Fetch the specific PurchaseMaster by its primary key
    purchase_master = get_object_or_404(PurchaseMaster, pk=pk)
    # Fetch all PurchaseDetails associated with the PurchaseMaster
    purchase_details = PurchaseDetail.objects.filter(purchase_master=purchase_master)
    return render(request, 'purchase_detail_view.html', {'purchase_master': purchase_master, 'purchase_details': purchase_details})

# Ajax endpoint to get item price
def get_item_price(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    return JsonResponse({'price': item.price})

# Ajax endpoint to get supplier details
def get_supplier_details(request, supplier_id):
    supplier = get_object_or_404(Supplier, id=supplier_id)
    return JsonResponse({'supplier_name': supplier.name, 'supplier_contact': supplier.contact})  # Add any other details needed



    #-----------------------------------------------------sales page-------------------------------------------------

def sales_page(request):




    context = {

    }    
    return render(request, 'sales.html', context)