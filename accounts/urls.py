from django.urls import path
from .views import *

urlpatterns=[
    # registration
    path(route='register/',view=register,name='register'),
    path(route='activate/<uidb64>/<token>/',view=activate,name='activate'),
    
    # user login and logout 
    path(route='login/',view=login,name='login'),
    path(route='destroy-session/',view=destroySession,name='destroy_session'),
    

    # dashboard related
    path(route='dashboard/',view=dashboard,name='dashboard'),
    path(route='edit_profile/',view=edit_profile,name='edit_profile'),
    path(route='orders/',view=orders,name='orders'),
    path(route='change_password/',view=change_password,name='change_password'),
    
    # forgotpassword
    path(route='forgotpassword/',view=forgotpassword,name='forgotpassword'),
    path(route='reset_password/<uidb64>/<token>/',view=reset_password,name='reset_password'),
    path(route='add_new_password/<uidb64>/<token>/',view=add_new_password,name='add_new_password'),
]