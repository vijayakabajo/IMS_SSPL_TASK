from django.shortcuts import render
from .models import Purchase

# Create your views here.
def purchase_page(request):
    return render(request, 'purchase.html')

def sales_page(request):
    return render(request, 'sales.html')

