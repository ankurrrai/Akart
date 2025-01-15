"""akart URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import views

from django.conf.urls.static import static #static imported for media files and url
from django.conf import settings #import setting from main project which is akart here...

urlpatterns = [
    # configure admin
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')), #dummy admin page and its track login attempt to prevent from hacking
    path('akart-akart-secret-admin-akart/', admin.site.urls), #main admin page to keep secret
    
    # akart project view
    path('',view=views.home,name='home'), 
    path('developer-profile/',view=views.developer,name='developer'),

    # configure all apps url
    path('store/',include('store.urls')), #included store app urls
    path('cart/',include('carts.urls')), #include cart app urls
    path('user/',include('accounts.urls')),#included accounts app urls
    path('order/',include('orders.urls')),#included orders app urls

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) #static to use media url
