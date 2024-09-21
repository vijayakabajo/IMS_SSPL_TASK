from django.urls import path
from . import views

urlpatterns = [
    path('purchase/', views.purchase_page, name='purchase'),
    path('sales/', views.sales_page, name='sales')
]