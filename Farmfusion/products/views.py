from django.http import HttpResponse
from django.shortcuts import render
from.forms import ProductForm
from.models import Product
# Create your views here.
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('Success')
    else:
         form = ProductForm()
    return render(request, 'components/form.html', {'form': form})
def detail_product(request,p_id):
    p=Product.objects.get(pk=p_id)
    return render(request, 'components/detail-product.html', {"p":p})
def update_product(request,p_id):
    p = Product.objects.get(pk=p_id)
    if request.method == 'POST':
        form = ProductForm(request.POST,instance=p)
        if form.is_valid():
            form.save()
            return HttpResponse('Success')
    else:
        form = ProductForm(instance=p)
    return render(request, 'components/form.html', {'form': form})
def delete_product(request,p_id):
    Product.objects.get(pk=p_id).delete()
    return HttpResponse('Success')