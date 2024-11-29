from django.http import HttpResponse
from django.shortcuts import render
from.forms import ProductForm
from.models import Product
# Create your views here.
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES)
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



from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Review
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
from django.db.models import Avg

def product_detail(request,p_id):
    product = get_object_or_404(Product, pk=p_id)
    reviews = product.reviews.all()
    average_rating= reviews.aggregate(Avg('rating'))['rating__avg'] if reviews else 0
    # average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] if reviews() else 0
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.product = product
                review.user = request.user
                review.save()
                return redirect('product_detail', p_id=product.id)
        else:
            return redirect('login')
    else:
        form = ReviewForm()

    return render(request, 'components/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'form': form,
        'average_rating': average_rating
    }

                  )


from django.urls import reverse
from django.http import HttpResponseRedirect

def redirect_to_product(request, product_id):
    return HttpResponseRedirect(reverse('product_detail', args=[product_id]))

