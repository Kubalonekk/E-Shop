
from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name='index'),
    path('about_us/', views.about, name='about'),
    path('products/', views.products, name='products'),
    path('products/<str:gender>/', views.products_gender, name='products_gender'),
    path('products/<str:gender>/<str:category>/',
         views.products_category, name='products_category'),
    path('contact/', views.contact, name='contact'),
    path('product/<str:slug>/', views.product, name='product'),
    path('add_item_to_order/<str:slug>/',
         views.add_item_to_order, name='add_item_to_order'),
    path('shopping_cart/', views.shopping_cart, name='shopping_cart'),
    path('add_single_item_to_cart/<int:id>/',
         views.add_single_item_to_cart, name="add_single_item_to_cart"),
    path('remove_single_item_from_cart/<int:id>/',
         views.remove_single_item_from_cart, name="remove_single_item_from_cart"),
    path('remove_item_from_cart/<int:id>/',
         views.remove_item_from_cart, name="remove_item_from_cart"),
    path('shopping_cart2/', views.shopping_cart2, name='shopping_cart2'),
    path('address_and_payment/', views.address_and_payment,
         name='address_and_payment'),
    path('payment_check/', views.payment_check, name="payment_successful"),
    path('remove_cupon/<int:id>/', views.remove_cupon, name="remove_cupon"),

    # dashboard
    path('dashboard/orders/', views.dashboard_orders, name="dashboard_orders"),
    path('dashboard/order/<int:id>/',
         views.dashboard_order, name="dashboard_order"),
    path('dashboard/items/', views.dashboard_items, name="dashboard_items"),
    path('dashboard/item/<int:id>/', views.dashboard_item, name="dashboard_item"),
    path('dashboard/add_item/', views.dashboard_add_item,
         name="dashboard_add_item"),
    path('dashboard/edit_item/<int:id>/',
         views.dashboard_edit_item, name="dashboard_edit_item"),
    path('dashboard/add_stock_item/<int:id>/',
         views.dashboard_add_stock_item, name="dashboard_add_stock_item"),

    # accounts
    path('register/', views.register, name='register'),
    path('signout/', views.signout, name="signout"),
    path('login_page/', views.login_page, name='login_page'),

    # payu integration
    path('create_payu_order/<int:order>/<int:customer>/<int:address>/',
         views.create_payu_order, name="create_payu_order"),
    path('payu_notification/', views.payu_notification, name="payu_notification")
]
