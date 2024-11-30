from django.http import HttpResponse
from django.shortcuts import render
from.forms import ProductForm
from.models import Product
from .models import Product, CartItem, Order, OrderItem
from django.contrib.auth.decorators import login_required
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



# For Review
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


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)

    if not created:
        cart_item.quantity += 1

    cart_item.save()

    return redirect('cart')


def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
    cart_item.delete()
    return redirect('cart')



def update_quantity(request, cart_item_id):

    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
        new_quantity = int(request.POST.get('quantity', 1))
        if new_quantity > 0:
            cart_item.quantity = new_quantity
            cart_item.save()
        else:
            cart_item.delete()
        return redirect('cart')
    return JsonResponse({'error': 'Invalid request method'}, status=400)


def checkout(request):
    user = request.user
    cart_items = CartItem.objects.filter(user=user)

    if cart_items.exists():

        order = Order.objects.create(user=user)


        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity
            )
        cart_items.delete()


        messages.success(request, 'Checkout successful!!')

        return redirect('order_history')
    else:
        messages.error(request, 'Your cart is empty. Please add items before checkout.')
        return redirect('cart')

def cart(request):

    cart_items = CartItem.objects.filter(user=request.user)

    total = sum(item.product.price * item.quantity for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'cart.html', context)