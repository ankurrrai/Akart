from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from store.models import Product,Variation
from .models import Cart,CartItem

from django.contrib.auth.decorators import login_required

def _cart_id(request):
    # collecting session from request either existing or created new
    cart_id=request.session.session_key
    if not cart_id:
        cart_id=request.session.create()
    return cart_id

def add_to_cart(request,product_id):

    product=Product.objects.get(id=product_id) #fetching product with its id
    product_variation=[]
    if request.method=='POST':
        i=1
        for item in request.POST:
            key=item.strip()
            key_value=request.POST[key].strip()
            if 'csrf' in key:
                continue

            # collect the variations from Varition Model
            variation=Variation.objects.get(product=product,variation_category__iexact=key,variation_value__iexact=key_value,is_active=True)
            product_variation.append(variation) #append all varition to use
        
        

    if request.user.is_authenticated:
        cart_item=CartItem.objects.filter(product=product,user=request.user) #check available product with refer to cart of user
    else:
        cart,created=Cart.objects.get_or_create(cart_id=_cart_id(request=request)) #either get the cart with cart_id (i.e session key) or create with it.
        cart_item=CartItem.objects.filter(product=product,cart=cart) #check available product with refer to cart of session
    
    '''
    If product in cart _items exist then loop all cart_items to check same variations available or not? If yes then increase the quantity of product and redirect  to cart page.
    If product is not available withing cart_items then create new one and with added variations

    '''

    if cart_item.exists():
        
        for item in cart_item:
            if product_variation == list(item.variations.all()):
                item.quantity+=1
                item.save()
                return redirect ('cart')

        
    if request.user.is_authenticated:
        cart_item=CartItem.objects.create(product=product,user=request.user,quantity=1)
    else:
        cart_item=CartItem.objects.create(product=product,cart=cart,quantity=1)
    if len(product_variation)>0:
        cart_item.variations.clear()
        for item in product_variation:
            cart_item.variations.add(item)
    cart_item.save()
    return redirect ('cart')
     

def remove_cart(request,product_id,cartItem_id):

    # collect cart from session id..
    # collect product from product which is from param 'product_id'
    # collect cart_item from cart_item_id from param 'cartItem_id'
    
    if request.user.is_authenticated:
        product=get_object_or_404(Product,id=product_id)
        cart_item=CartItem.objects.get(id=cartItem_id,user=request.user,product=product)
    else:
        cart=Cart.objects.get(cart_id=_cart_id(request=request))
        product=get_object_or_404(Product,id=product_id)
        cart_item=CartItem.objects.get(id=cartItem_id,cart=cart,product=product)

    # if quantity is more than 1 then reduce the quantity else delete it
    if cart_item.quantity>1:
        cart_item.quantity-=1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

def remove_cart_item(request,product_id,cartItem_id):

    # collect cart from session id..
    # collect product from product which is from param 'product_id'
    # collect cart_item from cart_item_id from param 'cartItem_id'
    if request.user.is_authenticated:
        product=get_object_or_404(Product,id=product_id)
        cart_item=CartItem.objects.get(id=cartItem_id,user=request.user,product=product)
    else:
        cart=Cart.objects.get(cart_id=_cart_id(request=request))
        product=get_object_or_404(Product,id=product_id)
        cart_item=CartItem.objects.get(id=cartItem_id,cart=cart,product=product)

    # delete product from cart_item
    cart_item.delete()
    return redirect('cart')


def load_cart(request,total=0,quantity=0,cart_items=None,grand_total=0,tax=0):
    try:
        
        if request.user.is_authenticated:
            cart_items=CartItem.objects.filter(user=request.user,is_active=True)
        else:
            cart=Cart.objects.get(cart_id=_cart_id(request=request)) # collect cart from using session
            cart_items=CartItem.objects.filter(cart=cart,is_active=True) # collect cart_items from using cart
        
        # calculate the total, tax and grand_total
        for cart_item in cart_items:
            total+=cart_item.product.price*cart_item.quantity
            quantity+=cart_item.quantity
        
        tax=(2*total)/100
        grand_total=total+tax
    except:
        pass

    # store require key and value with context to use in template
    context={
        'cart_items':cart_items,
        'total':total,
        'quantity':quantity,
        'tax':tax,
        'grand_total':grand_total


    }
    return render(request=request,template_name='store/cart.html',context=context)

@login_required(login_url='login')
def checkout(request,total=0,quantity=0,cart_items=None,grand_total=0,tax=0):
    try:
        
        if request.user.is_authenticated:
            cart_items=CartItem.objects.filter(user=request.user,is_active=True)
        else:
            cart=Cart.objects.get(cart_id=_cart_id(request=request)) # collect cart from using session
            cart_items=CartItem.objects.filter(cart=cart,is_active=True) # collect cart_items from using cart
        
        # calculate the total, tax and grand_total
        for cart_item in cart_items:
            total+=cart_item.product.price*cart_item.quantity
            quantity+=cart_item.quantity
        
        tax=(2*total)/100
        grand_total=total+tax
    except:
        pass

    # store require key and value with context to use in template
    context={
        'cart_items':cart_items,
        'total':total,
        'quantity':quantity,
        'tax':tax,
        'grand_total':grand_total


    }
    return render(request=request,template_name='store/checkout.html',context=context)