from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),


# CRUDSUPP
    path('suppliers/', views.supplier_page, name='supplier_page'),
    path('suppliers/<str:action>/<int:supplier_id>/', views.handle_supplier, name='handle_supplier'),


    # path('suppliers/add/', views.add_supplier, name='add_supplier'),
    # path('suppliers/edit/<int:supplier_id>/', views.edit_supplier, name='edit_supplier'),   #editsuppbyid
    # path('suppliers/delete/<int:supplier_id>/', views.delete_supplier, name='delete_supplier'),     #deletesuppbyid


# CRUDITEM
    path('items/', views.items_page, name='items_page'),
    path('items/<str:action>/<int:item_id>/', views.handle_items, name='handle_items'),



    # path('items/add/', views.add_item, name='add_item'),
    # path('items/edit/<int:item_id>/', views.edit_item, name='edit_item'),           #edititemsbyid
    # path('items/delete/<int:item_id>/', views.delete_item, name='delete_item'),   #deleteitemsbyid
]
