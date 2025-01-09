from django.urls import path
from .views import place_order,payments

urlpatterns=[
    path(route='place-order/',view=place_order,name='place-order'),
    path(route='payments/',view=payments,name='payments'),
]