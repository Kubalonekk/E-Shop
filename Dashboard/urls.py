
from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'Dashboard'

urlpatterns = [
  
    path('orders/', views.dashboard_orders, name="dashboard_orders"),
    path('order/<int:id>/',
         views.dashboard_order, name="dashboard_order"),
    path('items/', views.dashboard_items, name="dashboard_items"),
    path('item/<int:id>/', views.dashboard_item, name="dashboard_item"),
    path('add_item/', views.dashboard_add_item,
         name="dashboard_add_item"),
    path('edit_item/<int:id>/',
         views.dashboard_edit_item, name="dashboard_edit_item"),
    path('add_stock_item/<int:id>/',
         views.dashboard_add_stock_item, name="dashboard_add_stock_item"),
]
