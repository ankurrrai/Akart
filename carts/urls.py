from django.urls import path
from . import views
urlpatterns=[
    path('',view=views.load_cart,name='cart'),
    path('add_cart/<int:product_id>/',view=views.add_to_cart,name='add_cart'),
    path('remove_cart/<int:product_id>/',view=views.remove_cart,name='remove_cart'),
    path('remove_cart_item/<int:product_id>/',view=views.remove_cart_item,name='remove_cart_item')
]