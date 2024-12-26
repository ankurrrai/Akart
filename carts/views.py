from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from store.models import Product
from .models import Cart,CartItem

def _cart_id(request):
    # collecting session from request either existing or created new
    cart_id=request.session.session_key
    if not cart_id:
        cart_id=request.session.create()
    return cart_id

def add_to_cart(request,product_id):

    product=Product.objects.get(id=product_id) #fetching product with its id
    cart,created=Cart.objects.get_or_create(cart_id=_cart_id(request=request)) #either get the cart with cart_id (i.e session key) or create with it.

    try:
        cart_item=CartItem.objects.get(
            product=product,
            cart=cart
        )
        cart_item.quantity+=1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item=CartItem.objects.create(
            product=product,
            cart=cart,
            quantity=1
        )
        cart_item.save()
    return redirect('product_details',category_slug=product.category.slug,product_slug=product.slug)
     

def remove_cart(request,product_id):
    cart=Cart.objects.get(cart_id=_cart_id(request=request))
    product=get_object_or_404(Product,id=product_id)
    cart_item=CartItem.objects.get(cart=cart,product=product)

    if cart_item.quantity>1:
        cart_item.quantity-=1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

def remove_cart_item(request,product_id):
    cart=Cart.objects.get(cart_id=_cart_id(request=request))
    product=get_object_or_404(Product,id=product_id)
    cart_item=CartItem.objects.get(cart=cart,product=product)
    cart_item.delete()
    return redirect('cart')


def load_cart(request,total=0,quantity=0,cart_items=None,grand_total=0,tax=0):
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request=request))
        cart_items=CartItem.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items:
            total+=cart_item.product.price*cart_item.quantity
            quantity+=cart_item.quantity
        tax=(2*total)/100
        grand_total=total+tax
    except:
        pass
    context={
        'cart_items':cart_items,
        'total':total,
        'quantity':quantity,
        'tax':tax,
        'grand_total':grand_total


    }
    return render(request=request,template_name='store/cart.html',context=context)