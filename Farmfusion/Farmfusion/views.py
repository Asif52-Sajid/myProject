from django.shortcuts import render
from products.models import Product


def home(request):
    return render(request, 'home.html')
def product(request):
    products = Product.objects.all()
    return render(request,'product.html',{"products":products,})