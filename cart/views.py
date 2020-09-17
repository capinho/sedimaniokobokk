from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm,CartAddProductForm1

@login_required
@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    user= request.user
    product = get_object_or_404(Product, id=product_id)
    if user.profile.is_administration:
        form=CartAddProductForm1(request.POST,user)
    else:
        form = CartAddProductForm(request.POST,user)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('cart:cart_detail')

@login_required
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

@login_required
def cart_detail(request):
    cart = Cart(request)
    user=request.user
    # En utilisant for in, il commencera à itérer et appellera `__iter__`
    for item in cart:
        if user.profile.is_administration:
            item['update_quantity_form'] = CartAddProductForm1(
                initial={
                    'quantity': item['quantity'],
                    'update': True
                })
        else:
            item['update_quantity_form'] = CartAddProductForm(
                initial={
                    'quantity': item['quantity'],
                    'update': True
                })
    return render(request, 'cart/detail.html', {'cart': cart})
    
