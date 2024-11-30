"""
URL configuration for Farmfusion project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from django.urls import reverse
urlpatterns = [
    path('create-product',views.create_product,name='create-product'),
    path('detail-product/<int:p_id>', views.detail_product, name='detail-product'),
    path('update-product/<int:p_id>', views.update_product, name='update-product'),
    path('delete-product/<int:p_id>', views.delete_product, name='delete-product'),
    path('product_detail/<int:p_id>/', views.product_detail, name='product_detail'),

    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:cart_item_id>/', views.update_quantity, name='update_quantity'),
    path('checkout/', views.checkout, name='checkout'),
    path('cart/',views.cart,name='cart'),




]