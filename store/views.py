from django.shortcuts import render,get_object_or_404
from .models import Product
from category.models import Category

from carts.models import *
from carts.views import _cart_id

def store(request,category_slug=None):

    if category_slug is not None:
        categories=get_object_or_404(Category,slug=category_slug)
        products=Product.objects.filter(category=categories,is_available=True)

    else:
        products=Product.objects.all().filter(is_available=True)

    product_count=products.count()
    context={
        'products':products,
        'product_count':product_count,

    }
    
    return render(request=request,template_name='store/store.html',context=context)


def product_details(request,category_slug,product_slug):
    try:
        single_product=Product.objects.get(category__slug=category_slug,slug=product_slug)
        cart_exits=CartItem.objects.filter(cart__cart_id=_cart_id(request=request),product=single_product).exists()
    except Exception as e:
        raise e
    context={
        'single_product':single_product,
        'cart_exits':cart_exits,
    }
    return render(request=request,template_name='store/product_details.html',context=context)