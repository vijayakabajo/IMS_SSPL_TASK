# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('report/', views.report_page , name='report_page'),

]