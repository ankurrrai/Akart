from django.urls import path
from .views import *

urlpatterns=[
    path(route='register/',view=register,name='register'),
    path(route='login/',view=login,name='login'),
    path(route='destroy-session/',view=destroySession,name='destroy_session'),
    path(route='activate/<uidb64>/<token>/',view=activate,name='activate')
]