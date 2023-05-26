
from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

app_name = 'Api'

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('products/', views.products, name="products"),
    path('products/<str:gender>/', views.products_gender, name='products_gender'),
    path('products/<str:gender>/<str:category>/',
        views.products_category, name='products_category'),
    path('add-item/<str:slug>/', views.add_item_to_order, name="item-add_item_to_order"),
    path('product/<str:slug>/', views.product, name='product'),
    path('shopping_cart/', views.shopping_cart, name='shopping_cart'),
    path('single_item_cart/<int:id>/',
        views.single_item_cart, name="single_item_cart"),
    path('product_images/<str:slug>/', views.product_images, name='product_images'),
    path('remove_item_from_cart/<int:id>/',
        views.remove_item_from_cart, name="remove_item_from_cart"),
    path('test/', views.test, name="test"),
    path('sizes/<str:slug>/', views.sizes, name="sizes"),
    path('order/', views.order, name="order"),
    path('cupon/', views.cupon, name="cupon"),
    path('categories/<str:gender>/', views.categories, name='categories'),
    
    
     
       
     
]
