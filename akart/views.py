from django.http import HttpResponse
from django.shortcuts import render,redirect
from store.models import Product,RatingReview
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator

# this is just render index.html with all available products
def home(request):
    products=Product.objects.all().filter(is_available=True).order_by('-created_date')
    

    # paginator code added
    paginator=Paginator(products,27)
    page=request.GET.get('page')
    page_products=paginator.get_page(page)

    context={
        'products':page_products,
        
    }
    
    return render(request=request,template_name='index.html',context=context)
 
def developer(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    return render(request=request,template_name='developer/contact.html')