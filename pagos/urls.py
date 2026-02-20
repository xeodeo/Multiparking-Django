from django.urls import path
from . import views

urlpatterns = [
    path('', views.PagosListView.as_view(), name='admin_pagos'),
]
