from django.urls import path
from . import views
urlpatterns=[
    path('',view=views.load_cart,name='cart'), #this path is use to load the cart page
    path('add_cart/<int:product_id>/',view=views.add_to_cart,name='add_cart'), # this path is used to add_to_cart, In this product_id is require
    path('remove_cart/<int:product_id>/<int:cartItem_id>/',view=views.remove_cart,name='remove_cart'), # this path is used to reduce the quantity of product, In this product_id and cart_item id is require
    path('remove_cart_item/<int:product_id>/<int:cartItem_id>/',view=views.remove_cart_item,name='remove_cart_item'), # this path is used to delete a product, In this product_id and cart_item id is require

    # checkout
    path(route='checkout/',view=views.checkout,name='checkout')
]