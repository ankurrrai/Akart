#render: it is used to render the template
#get_object_or_404: It help to find object from model class else redirect to error page
from django.shortcuts import render,get_object_or_404

# models import from different app based on use
from .models import Product
from category.models import Category
from carts.models import * 
from carts.views import _cart_id 

from django.http import HttpResponse

# import Q to make somplex queries
from django.db.models import Q

# paginator : please use documentation of django
from django.core.paginator import PageNotAnInteger,Paginator,EmptyPage

# render products by category slug and if category slug is missing in param then render all product to the store
def store(request,category_slug=None):

    if category_slug is not None:
        categories=get_object_or_404(Category,slug=category_slug)
        products=Product.objects.filter(category=categories,is_available=True).order_by('id')

    else:
        products=Product.objects.all().filter(is_available=True).order_by('id')

    # paginator code added
    paginator=Paginator(products,27)
    page=request.GET.get('page')
    page_products=paginator.get_page(page)


    # all product counts
    product_count=products.count()
    context={
        'products':page_products,
        'product_count':product_count,

    }
    
    return render(request=request,template_name='store/store.html',context=context)


# rebder the product details html file wrt category and product slug in param
def product_details(request,category_slug,product_slug):
    try:
        single_product=Product.objects.get(category__slug=category_slug,slug=product_slug)
        cart_exits=CartItem.objects.filter(cart__cart_id=_cart_id(request=request),product=single_product).exists() #check this product is available to cart or not
    except Exception as e:
        raise e
    context={
        'single_product':single_product,
        'cart_exits':cart_exits,
    }
    return render(request=request,template_name='store/product_details.html',context=context)

def serach_product(request):
    products=None
    product_count=0
    if 'keyword' in request.GET:
        keyword=request.GET['keyword']
        keyword=keyword.strip()
        products=Product.objects.order_by('modified_date').filter(Q(category__slug__icontains=keyword) | Q(slug__icontains=keyword) | Q(description__icontains=keyword) | Q(product_name__icontains=keyword) )
        product_count=products.count()
    
    context={
        'products':products,
        'product_count':product_count,

    }
    
    return render(request=request,template_name='store/store.html',context=context)
