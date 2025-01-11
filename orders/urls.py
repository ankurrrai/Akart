from django.urls import path
from .views import place_order,payments,order_complete

urlpatterns=[
    path(route='place-order/',view=place_order,name='place-order'),
    path(route='payments/',view=payments,name='payments'),
    path(route='order_complete/',view=order_complete,name='order_complete'),
]