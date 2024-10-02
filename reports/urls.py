# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('report/', views.report_page , name='report_page'),
    path('detail_report/', views.detailed_list , name='detail_report_page'),
    # path('detailed-list/', views.detailed_list, name='detailed_list'),
]