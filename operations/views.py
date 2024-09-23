from django.shortcuts import render
from .models import PurchaseMaster

# Create your views here.
# purchase_page 
def purchase_page(request):
    return render(request, 'purchase.html')
# sales_page
def sales_page(request):
    return render(request, 'sales.html')

