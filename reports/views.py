from django.shortcuts import render
from operations.models import PurchaseDetail,SalesDetail
from master.models import Item
from django.db.models import Sum

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


def item_report(request):




    context = {

    }
    return render(request, 'item_report.html', context)



