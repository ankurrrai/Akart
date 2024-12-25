
from django.urls import path
from . import views
urlpatterns = [
    path('',view=views.store,name='store'),
    path('<slug:category_slug>/',view=views.store,name='product_by_category'),
    path('<slug:category_slug>/<slug:product_slug>',view=views.product_details,name='product_details'),
]
