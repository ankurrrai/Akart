from django.http import HttpResponse
from django.shortcuts import render,redirect
from store.models import Product,RatingReview
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from carts.views import _cart_id
from carts.views import Cart

def home(request):

    # check the session
    '''
        If session exists the pass display disclimar popup like this all image not related to us
        This logic allow to show only one time for each session 
    '''
    new_session=False
    try:
        cart_id=_cart_id(request=request)
        cart_session_exist=Cart.objects.filter(cart_id=cart_id).exists()
        if not cart_session_exist:
            new_session=True
            cart=Cart.objects.create(cart_id=cart_id)
    except:
        new_session=False
    

    # collect all products and use paginator to split it into multiple page
    products=Product.objects.all().filter(is_available=True).order_by('-created_date')
    

    # paginator code added
    paginator=Paginator(products,27)
    page=request.GET.get('page')
    page_products=paginator.get_page(page)

    context={
        'products':page_products,
        'new_session':new_session,
        
    }
    
    return render(request=request,template_name='index.html',context=context)
 
# rendering details of devloper linkedIn profile
def developer(request):
    if request.user.is_authenticated:
        return redirect('home')
    context={
        'username':'ankurrrai'
    }
    return render(request=request,template_name='developer/contact.html',context=context)