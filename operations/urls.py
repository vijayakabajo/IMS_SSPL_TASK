# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('purchase/', views.purchase_page, name='purchase-page'),
    path('purchases/', views.purchase_master_list, name='purchase_master_list'),
    path('purchases/<int:pk>/', views.purchase_detail_view, name='purchase_detail_view'),
    path('sales/', views.sales_page, name='sales-page'),
]
