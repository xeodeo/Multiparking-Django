from django.urls import path
from . import views

urlpatterns = [
    path('', views.PagosListView.as_view(), name='admin_pagos'),
    path('recibo/<int:pk>/', views.ReciboView.as_view(), name='recibo_pago'),
]
