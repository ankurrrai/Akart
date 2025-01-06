from .models import *
from .views import _cart_id

# this is context_processor for cart count
def get_cart_count(request):
    cart_count=0
    if 'admin' in request.path:
        return {}
    try:
        if request.user.is_authenticated:
            cart_items=CartItem.objects.filter(user=request.user)
        else:
            cart_items=CartItem.objects.filter(cart__cart_id=_cart_id(request=request))
        for cart_item in cart_items:
            cart_count+=cart_item.quantity
    except Cart.DoesNotExist:
        cart_count=0
    return dict(cart_count=cart_count)
    