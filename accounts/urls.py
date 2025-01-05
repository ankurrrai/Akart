from django.urls import path
from .views import *

urlpatterns=[
    # registration
    path(route='register/',view=register,name='register'),
    path(route='activate/<uidb64>/<token>/',view=activate,name='activate'),
    
    # user login and logout 
    path(route='login/',view=login,name='login'),
    path(route='destroy-session/',view=destroySession,name='destroy_session'),
    

    # dashboard
    path(route='dashboard/',view=dashboard,name='dashboard'),
    
    # forgotpassword
    path(route='forgotpassword/',view=forgotpassword,name='forgotpassword'),
    path(route='reset_password/<uidb64>/<token>/',view=reset_password,name='reset_password'),
    path(route='add_new_password/<uidb64>/<token>/',view=add_new_password,name='add_new_password'),
]