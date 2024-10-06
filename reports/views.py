from django.shortcuts import render
from operations.models import PurchaseDetail, SalesDetail
from master.models import Item
from django.db.models import Sum, Q
from django.utils.dateparse import parse_date
from datetime import datetime
from django.http import JsonResponse
from django.db import connection


def report_page(request):
    item_name = request.GET.get('item', '')
    search_input = request.GET.get('search_input', '')

    sql = """
        SELECT i.id, i.name,
            COALESCE(SUM(p.quantity), 0) AS total_purchased,
            COALESCE(SUM(s.quantity), 0) AS total_sold,
            COALESCE(SUM(p.quantity), 0) - COALESCE(SUM(s.quantity), 0) AS available_stock
        FROM master_item i
        LEFT JOIN operations_purchasedetail p ON p.item_id_id = i.id
        LEFT JOIN operations_salesdetail s ON s.item_id = i.id
        WHERE i.status = 1
    """


    filters = []
    if search_input:
        filters.append(f"i.name ILIKE '%{search_input}%'")
    elif item_name:
        filters.append(f"i.name = '{item_name}'")

    if filters:
        sql += " AND " + " AND ".join(filters)

    sql += " GROUP BY i.id, i.name;"

    with connection.cursor() as cursor:
        cursor.execute(sql)
        stock_data = cursor.fetchall()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'stock_data': stock_data})

    context = {
        'stock_data': stock_data
    }
    return render(request, 'stock_report.html', context)




#------------------------------------------detail list view-----------------------------------------------------------
from django.db import connection

def detailed_list(request):
    items = Item.objects.filter(status=1)

    item_name = request.GET.get('item', '')
    from_date = request.GET.get('fromdate', '1900-01-01')
    to_date = request.GET.get('todate', str(datetime.now().date())) 
    report_type = request.GET.get('type', 'purchase')

    from_date = parse_date(from_date) or datetime.strptime('1900-01-01', '%Y-%m-%d').date()
    to_date = parse_date(to_date) or datetime.now().date()

    stock_data = []

    query = ''
    params = []

    if report_type == 'purchase':
        query = '''
            SELECT i.name AS item_name, pd.quantity, pd.items_total, pm.created_at, s.name AS supplier_or_customer
            FROM operations_purchasedetail pd
            JOIN master_item i ON pd.item_id_id = i.id
            JOIN operations_purchasemaster pm ON pd.purchase_master_id = pm.id
            JOIN master_supplier s ON pm.supplier_id_id = s.id
            WHERE pd.created_at BETWEEN %s AND %s 
        '''
        params = [from_date, to_date]

        if item_name:
            query += ' AND i.name LIKE %s'
            params.append(f'%{item_name}%')

    elif report_type == 'sales':
        query = '''
            SELECT i.name AS item_name, sd.quantity, sd.items_total, sm.bill_date AS created_at, s.name AS supplier_or_customer
            FROM operations_salesdetail sd
            JOIN master_item i ON sd.item_id = i.id
            JOIN operations_salesmaster sm ON sd.sales_master_id = sm.id
            JOIN master_supplier s ON sm.seller_id = s.id
            WHERE sm.bill_date BETWEEN %s AND %s
        '''
        params = [from_date, to_date]

        if item_name:
            query += ' AND i.name LIKE %s'
            params.append(f'%{item_name}%')

    with connection.cursor() as cursor:
        cursor.execute(query, params)
        rows = cursor.fetchall()

    for row in rows:
        stock_data.append({
            'item_name': row[0],
            'quantity': row[1],
            'total': row[2],
            'created_at': row[3].strftime('%d-%m-%Y'),
            'supplier_or_customer': row[4]
        })

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'stock_data': stock_data})

    context = {
        'stock_data': stock_data,
        'items': items
    }

    return render(request, 'detail_report.html', context)
