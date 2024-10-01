# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('purchase/', views.purchase_page, name='purchase-page'),

    path('get-item-price/<int:item_id>/', views.get_item_price, name='get_item_price'),
    path('get-supplier-details/<int:supplier_id>/', views.get_supplier_details, name='get_supplier_details'),
    # path('purchase/remove-item/<int:item_id>/', views.remove_item, name='remove_item'),
    path('purchases/', views.purchase_master_list, name='purchase_master_list'),
    path('purchases/<int:pk>/', views.purchase_detail_view, name='purchase_detail_view'),
    path('remove-item/<int:item_id>/', views.remove_item, name='remove_item'),
    # path('sales/', views.sales_page, name='sales-page'),
    path('sales/create/', views.sales_page, name='sales-create'),
    path('remove-item-sales/<int:item_id>/', views.remove_item_sales_temp, name='remove_item_sales'),
    path('sales/', views.sales_master_list, name='sales_master_list'),
    path('sales/<int:pk>/', views.sales_detail_view, name='sales_detail_view'),
    path('available-stock/<int:item_id>/', views.get_available_stock , name='available_stock'),
]
