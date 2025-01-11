#render: it is used to render the template
#get_object_or_404: It help to find object from model class else redirect to error page
from django.shortcuts import render,get_object_or_404,redirect

# models import from different app based on use
from .models import Product,RatingReview
from category.models import Category
from carts.models import * 
from carts.views import _cart_id 
from .forms import ReviewForm
from django.contrib import messages
from django.http import HttpResponse
from orders.models import OrderProduct
from orders.views import get_client_ip
from django.contrib.auth.decorators import login_required

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
        single_product=Product.objects.get(category__slug=category_slug,slug=product_slug) #collect product details by using param such that 'category_slug' and 'product_slug'.
        cart_exits=CartItem.objects.filter(cart__cart_id=_cart_id(request=request),product=single_product).exists() #check this product is available to cart or not
        reviews=RatingReview.objects.filter(product=single_product)
    except Exception as e:
        raise e
    context={
        'single_product':single_product,
        'cart_exits':cart_exits,
        'reviews':reviews,
    }
    return render(request=request,template_name='store/product_details.html',context=context)

def serach_product(request):
    products=None
    product_count=0
    if 'keyword' in request.GET:
        #collect the keyword and  remove the white spaces
        keyword=request.GET['keyword'] 
        keyword=keyword.strip() 

        # collect all products form Query
        products=Product.objects.order_by('modified_date').filter(Q(category__category_name__icontains=keyword) | Q(category__slug__icontains=keyword) |
         Q(slug__icontains=keyword) | Q(description__icontains=keyword) | Q(product_name__icontains=keyword) )
        product_count=products.count()
    
    context={
        'products':products,
        'product_count':product_count,

    }
    
    return render(request=request,template_name='store/store.html',context=context)

@login_required(login_url='login')
def sumbit_review(request,product_id):
    url=request.META.get('HTTP_REFERER')
    if request.method=='POST':
        order_product=OrderProduct.objects.filter(user=request.user,product__id=product_id).exists()
        if not order_product:
            messages.error(request=request,message='You are not permiited to sumbit the review. To do this please purchase the product!!')
            return redirect(url)
        try:
            review=RatingReview.objects.get(user__id=request.user.id,product__id=product_id)
            form=ReviewForm(request.POST,instance=review)
            form.save()
            messages.success(request=request,message='Thank you for contributed. Your review has updated!')
            return redirect(url)
        except RatingReview.DoesNotExist:
            form=ReviewForm(request.POST)
            if form.is_valid():
                review=RatingReview()
                review.subject=form.cleaned_data['subject']
                review.review=form.cleaned_data['review']
                review.rating=form.cleaned_data['rating']
                review.ip=get_client_ip(request=request)
                review.product_id=product_id
                review.user_id=request.user.id
                review.save()
                messages.success(request=request,message='Thank you for contributed. Your review has submitted!')
                return redirect(url)
            messages.error(request=request,message='You are not permiited to sumbit the review!')
            return redirect(url)
    return redirect('home')
