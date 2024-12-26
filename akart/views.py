from django.http import HttpResponse
from django.shortcuts import render
from store.models import Product
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
# this is just render index.html with all available products
def home(request):
    products=Product.objects.all().filter(is_available=True)

    # paginator code added
    paginator=Paginator(products,27)
    page=request.GET.get('page')
    page_products=paginator.get_page(page)

    context={
        'products':page_products,
    }
    
    return render(request=request,template_name='index.html',context=context)
 