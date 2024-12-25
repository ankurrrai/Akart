from .models import *
from .views import _cart_id

def get_cart_count(request):
    cart_count=0
    if 'admin' in request.path:
        return {}
    try:
        cart_items=CartItem.objects.filter(cart__cart_id=_cart_id(request=request))
        for cart_item in cart_items:
            cart_count+=cart_item.quantity
    except Cart.DoesNotExist:
        cart_count=0
    return dict(cart_count=cart_count)
    