# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('purchase/', views.purchase_page, name='purchase-page'),
    path('purchases/', views.purchase_master_list, name='purchase_master_list'),
    path('get-item-price/<int:item_id>/', views.get_item_price, name='get_item_price'),
    path('get-supplier-details/<int:supplier_id>/', views.get_supplier_details, name='get_supplier_details'),
    path('purchases/<int:pk>/', views.purchase_detail_view, name='purchase_detail_view'),
    path('sales/', views.sales_page, name='sales-page'),
]
