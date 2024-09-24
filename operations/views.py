# views.py
from django.shortcuts import render, redirect
from django.db import transaction
from .models import PurchaseMaster, PurchaseDetail, TempTable
from master.models import Supplier, Item
from .forms import TempTableForm, PurchaseMasterForm

def purchase_page(request):
    temp_items = TempTable.objects.all()   #getting temp tables details
    purchase_form = PurchaseMasterForm()
    temp_form = TempTableForm()

    if request.method == 'POST':             # Adding items to the temp table
        if 'add_item' in request.POST:
            temp_form = TempTableForm(request.POST)
            if temp_form.is_valid():
                temp_item = temp_form.save(commit=False)
                temp_item.items_total = temp_item.item_id.price * temp_item.quantity
                temp_item.save()
                return redirect('purchase-page')

        if 'finalize_purchase' in request.POST:                     
            purchase_form = PurchaseMasterForm(request.POST)         # Finalizing the purchase
            if purchase_form.is_valid():
                with transaction.atomic():                                       # transaction.atomic()*
                    purchase_master = purchase_form.save(commit=False)          #only validates, it won't commit changes
                    purchase_master.sub_total = sum(item.items_total for item in temp_items)
                    purchase_master.save()

                    # Save PurchaseDetails
                    for temp_item in temp_items:
                        PurchaseDetail.objects.create(
                            purchase_master=purchase_master,
                            item_id=temp_item.item_id,
                            quantity=temp_item.quantity,
                            items_total=temp_item.items_total
                        )

                    # Clear TempTable after finalizing the purchase
                    TempTable.objects.all().delete()

                return redirect('purchase-page')

    context = {
        'purchase_form': purchase_form,
        'temp_form': temp_form,
        'temp_items': temp_items,
    }
    return render(request, 'purchase.html', context)
