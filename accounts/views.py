from django.shortcuts import render,redirect
from .forms import RegisterForm

def register(request):
    form=RegisterForm()
    context={
        'form':form,
    }
    return render(request=request,template_name='accounts/register.html',context=context)

def login(request):
    context={}
    return render(request=request,template_name='accounts/login.html',context=context)

def destroySession(request):
    context={}
    return redirect('home')
