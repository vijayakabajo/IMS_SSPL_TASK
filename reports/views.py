from django.shortcuts import render
from operations.models import PurchaseDetail, SalesDetail
from master.models import Item
from django.db.models import Sum
from django.db.models import Q
from django.utils.dateparse import parse_date
from datetime import datetime
from django.http import JsonResponse
from django.db import connection

from django.db import connection

def report_page(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT i.id, i.name,
                COALESCE(SUM(p.quantity), 0) AS total_purchased,
                COALESCE(SUM(s.quantity), 0) AS total_sold,
                COALESCE(SUM(p.quantity), 0) - COALESCE(SUM(s.quantity), 0) AS available_stock
            FROM master_item i
            LEFT JOIN operations_purchasedetail p ON p.item_id_id = i.id
            LEFT JOIN operations_salesdetail s ON s.item_id = i.id
            WHERE i.status = 1
            GROUP BY i.id, i.name;
        """)
        stock_data = cursor.fetchall()

    context = {
        'stock_data': [
            {
                'item_name': row[1],
                'total_purchased': row[2],
                'total_sold': row[3],
                'available_stock': row[4]
            }
            for row in stock_data
        ]
    }

    return render(request, 'stock_report.html', context)







def detailed_list(request):
    items = Item.objects.filter(status=1)
    
    # Get query params
    item_name = request.GET.get('item', '')
    from_date = request.GET.get('fromdate', '1900-01-01') 
    to_date = request.GET.get('todate', str(datetime.now().date())) 
    report_type = request.GET.get('type', 'purchase')

    from_date = parse_date(from_date) or datetime.strptime('1900-01-01', '%Y-%m-%d').date()
    to_date = parse_date(to_date) or datetime.now().date()

    stock_data = []

    if report_type == 'purchase':
        # Fetch purchase data
        purchases = PurchaseDetail.objects.filter(created_at__date__range=[from_date, to_date]).order_by('-created_at')

        if item_name:
            purchases = purchases.filter(item_id__name__icontains=item_name)

        for purchase in purchases:
            stock_data.append({
                'item_name': purchase.item_id.name,
                'quantity': purchase.quantity,
                'total': purchase.items_total,
                'created_at': purchase.created_at.strftime('%d-%m-%Y'),
                'supplier_or_customer': purchase.purchase_master.supplier_id.name
            })

    elif report_type == 'sales':
        # Fetch sales data
        sales = SalesDetail.objects.filter(created_at__date__range=[from_date, to_date]).order_by('-created_at')

        if item_name:
            sales = sales.filter(item_id__name__icontains=item_name)

        for sale in sales:
            stock_data.append({
                'item_name': sale.item.name,
                'quantity': sale.quantity,
                'total': sale.items_total,
                'created_at': sale.created_at.strftime('%d-%m-%Y'),  #will change it to bill_date
                'supplier_or_customer': sale.sales_master.seller.name
            })

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'stock_data': stock_data})

    context = {
        'stock_data': stock_data,
        'items': items
    }

    return render(request, 'detail_report.html', context)