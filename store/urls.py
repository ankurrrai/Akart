
from django.urls import path
from . import views
urlpatterns = [
    path('',view=views.store,name='store'),
    path('category/<slug:category_slug>/',view=views.store,name='product_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/',view=views.product_details,name='product_details'),
    path(route='search/',view=views.serach_product,name='serach_product')
]
