from .models import Category

def categories_list(request):
    categories=Category.objects.all()
    return dict(categories=categories)