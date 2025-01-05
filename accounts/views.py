from django.shortcuts import render,redirect
from .forms import RegisterForm
from .models import Account
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse

# USER ACTIVATION
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method=='POST':
        form=RegisterForm(request.POST)
        if form.is_valid():
            try:
                first_name=form.cleaned_data['first_name']
                last_name=form.cleaned_data['last_name']
                phone_number=form.cleaned_data['phone_number']
                email=form.cleaned_data['email']
                password=form.cleaned_data['password']
                username=email.split('@')[0]+'1'
                user=Account.objects.create_user(email=email,first_name=first_name,last_name=last_name,username=username,password=password)
                user.phone_number=phone_number
                user.save()
                # ACTIVATION email
                
                subject_name='AKART | Verification email!!'
                message=render_to_string(template_name='accounts/email_activation.html',context={
                    'domain':get_current_site(request=request),
                    'user':user,
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user)
                })
                send_email=EmailMessage(subject=subject_name,body=message,to=[email])
                send_email.send()
                
                # messages.success(request=request,message='Email Sent')
                return redirect('../login/?validation=True&email='+str(email.strip()))
            except Exception as e:
                messages.error(request=request,message=e)
                return  redirect('register')
            
    else:
        form=RegisterForm()
    context={
        'form':form,
    }
    return render(request=request,template_name='accounts/register.html',context=context)

def login(request):

    # check the authentication
    if request.user.is_authenticated:
        return redirect('home')

    # if user is sumbit the form 
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']

        # do authenticate
        user=auth.authenticate(request=request,email=email,password=password)
        
        # if user has provide valid details login to the portal else throw an error message
        if not (user is None):
            auth.login(request=request,user=user)
            return redirect(request.GET.get('next','home'))
        else:
            messages.error(request=request,message='Email or password is incorrect!')
            return redirect('login')

    return render(request=request,template_name='accounts/login.html')

@login_required(login_url='login')
def destroySession(request):
    # call the decorater to do logout...
    auth.logout(request=request)
    messages.success(request=request,message='Logout Successfully!')
    return redirect('login')

# to activate account by verify an email of user
def activate(request,uidb64,token):
    try:
        # decode user id from param
        uid=urlsafe_base64_decode(uidb64).decode()
        user=Account.objects.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user=None

    # if user is in accounts and user token is valid the activate the account
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        messages.success(request=request,message='Email verification is done. Kindly login to your account!!')
        return redirect('login')
    
    # if not then pass a error meassge to register page
    messages.error(request=request,message='Invalid activation link')
    return redirect('register')


# load dashboard
@login_required(login_url='login')
def dashboard(request):
    return render(request=request,template_name='accounts/dashboard.html')


def forgotpassword(request):
    # to prevent for open url when client is logged in.
    if request.user.is_authenticated:
        return redirect('home')
    
    # when user sumbit form request...
    if request.method =='POST':
        
        # filter user with provided email
        user=Account.objects.filter(email__iexact=request.POST['email'])
        
        if user.exists():

            # if user exists then send an reset_email by using with tokens and primary key
            user=Account.objects.get(email__iexact=request.POST['email'])
            message=render_to_string(template_name='accounts/reset_password.html',context={
                'domain':get_current_site(request=request),
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
                'user':user
            })
            subject_name='Reset your password'
            email=EmailMessage(subject=subject_name,body=message,to=[user.email])
            email.send()
            messages.success(request=request,message="Reset link sent to your register email!")
            return redirect('login')
        else:
            # error messages
            messages.error(request=request,message="Account doesn't exist!")
            return redirect('forgotpassword')
    # render forgotpassword page
    return render(request=request,template_name='accounts/forgotpassword.html')



def reset_password(request,uidb64,token):
    
    # to prevent for open url when client is logged in.
    if request.user.is_authenticated:
        return redirect('home')

    # collect user informations from tokens and primary key i.e pk
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=Account.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user=None
    
    #if user has details are matched with tokens then update a given password
    if user is not None and default_token_generator.check_token(user,token):
        context={
                'domain':get_current_site(request=request),
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
                'user':user
            }
        # collect query value to display messages alerts
        if request.GET.get('has_error')!='Yes':
            messages.success(request=request,message='Link Verified! Update your password')
        return render(request=request,template_name='accounts/add_new_password.html',context=context)
    
    # return with error messages
    messages.error(request=request,message='Reset link is not valid!')
    return redirect('forgotpassword')
    


def add_new_password(request,uidb64,token):

    # to prevent for open url when client is logged in.
    if request.user.is_authenticated:
        return redirect('home')

    # check the form method
    if request.method=='POST':

        # if user has not provide password and confirm password then return to previous i.e same form..
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request=request,message='Password does not match!')
            return redirect(request.POST['previous']+'?has_error=Yes')

        # collect user informations from tokens and primary key i.e pk
        try:
            uid=urlsafe_base64_decode(uidb64).decode()
            user=Account.objects.get(pk=uid)
        except (TypeError,ValueError,OverflowError,Account.DoesNotExist):
            user=None
        
        #if user has details are matched with tokens then update a given password
        if user is not None and default_token_generator.check_token(user,token):
            user.set_password(password)
            user.save()
            messages.success(request=request,message='Password updated successfully!')
            return redirect('login')
        
        # return error messages
        messages.error(request=request,message='Something went wrong!')
        return redirect('forgotpassword')
    else:
        messages.error(request=request,message='Something went wrong!')
        return redirect('login')
