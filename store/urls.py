
from django.urls import path
from . import views
urlpatterns = [
    path('',view=views.store,name='store'), #render store page with all available product
    path('sumbit-review/<int:product_id>/',view=views.sumbit_review,name='sumbit_review'),
    path('category/<slug:category_slug>/',view=views.store,name='product_by_category'), #render store page with all product within selected category.
    path('category/<slug:category_slug>/<slug:product_slug>/',view=views.product_details,name='product_details'), #render project_details with selected product
    path(route='search/',view=views.serach_product,name='serach_product'), #render store page with all found products with keyword such in category and product
]
