from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from cart.forms import CartAddProductForm,CartAddProductForm1
from .models import Category, Product

@login_required
def product_list(request, category_slug=None):
    user=request.user
    category = None
    if user.profile.is_administration:
        categories = Category.objects.all()
    else:
        categories = Category.objects.all().exclude(name='Poulets frais')    
    if user.profile.is_administration:
        products = Product.objects.filter(available=True)
    else:
        products = Product.objects.filter(available=True).exclude(category__name='Poulets frais')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})

@login_required
def product_detail(request, product_id, slug):
    if request.user.profile.is_administration:
        product = get_object_or_404(Product,
                                    #~Q(name='Poulets frais'),
                                    id=product_id,
                                    slug=slug,
                                    available=True)
    else:
        product = get_object_or_404(Product,
                                    ~Q(category__name='Poulets frais'),
                                    id=product_id,
                                    slug=slug,
                                    available=True)
    if request.user.profile.is_administration:
        cart_product_form = CartAddProductForm1()
    else:
        cart_product_form = CartAddProductForm()
    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form})
