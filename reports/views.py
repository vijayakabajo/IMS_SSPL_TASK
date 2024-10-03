from django.shortcuts import render
from operations.models import PurchaseDetail, SalesDetail
from master.models import Item
from django.db.models import Sum
from django.db.models import Q
from django.utils.dateparse import parse_date
from datetime import datetime
from django.http import JsonResponse

def report_page(request):
    items = Item.objects.filter(status=1)
    stock_data = []
    for item in items:
        #quantity purchased
        total_purchased = PurchaseDetail.objects.filter(item_id=item.id).aggregate(
            total_purchased=Sum('quantity')
        )['total_purchased'] or 0
        
        
        #quantity sold
        total_sold = SalesDetail.objects.filter(item_id=item.id).aggregate(
            total_sold=Sum('quantity')
        )['total_sold'] or 0
        
        # Available stock
        available_stock = total_purchased - total_sold

        stock_data.append({
            'item_name': item.name,
            'total_purchased': total_purchased,
            'total_sold': total_sold,
            'available_stock': available_stock
        })

    context = {
        'stock_data': stock_data,
    }
    return render(request,'stock_report.html', context)





def detailed_list(request):
    items = Item.objects.filter(status=1)
    
    # Get query params
    item_name = request.GET.get('item', '')
    from_date = request.GET.get('fromdate', '1900-01-01')  # Default to earliest date
    to_date = request.GET.get('todate', str(datetime.now().date()))  # Default to current date
    report_type = request.GET.get('type', 'purchase')  # Default to purchase type

    # Convert string to date
    from_date = parse_date(from_date) or datetime.strptime('1900-01-01', '%Y-%m-%d').date()
    to_date = parse_date(to_date) or datetime.now().date()

    stock_data = []

    if report_type == 'purchase':
        # Fetch purchase data
        purchases = PurchaseDetail.objects.filter(created_at__date__range=[from_date, to_date])

        if item_name:
            purchases = purchases.filter(item_id__name__icontains=item_name)

        for purchase in purchases:
            stock_data.append({
                'item_name': purchase.item_id.name,  # Updated for ForeignKey
                'quantity': purchase.quantity,
                'total': purchase.items_total,
                'created_at': purchase.created_at,
                'supplier_or_customer': purchase.purchase_master.supplier_id.name
            })

    elif report_type == 'sales':
        # Fetch sales data
        sales = SalesDetail.objects.filter(created_at__date__range=[from_date, to_date])

        if item_name:
            sales = sales.filter(item_id__name__icontains=item_name)

        for sale in sales:
            stock_data.append({
                'item_name': sale.item.name,
                'quantity': sale.quantity,
                'total': sale.items_total,
                'created_at': sale.created_at,
                'supplier_or_customer': sale.sales_master.seller.name
            })

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'stock_data': stock_data})

    # Otherwise, render the template normally
    context = {
        'stock_data': stock_data,
        'items': items
    }

    return render(request, 'detail_report.html', context)