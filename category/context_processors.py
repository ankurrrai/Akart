from .models import Category

# all avaialble categories
def categories_list(request):
    categories=Category.objects.all()
    return dict(categories=categories)