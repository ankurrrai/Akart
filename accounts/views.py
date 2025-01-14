from django.shortcuts import render,redirect,get_object_or_404
from .forms import RegisterForm,UserForm,UserProfileForm
from .models import Account,UserDetails
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse


# load cartview and cart models
from carts.views import _cart_id
from carts.models import Cart,CartItem
from orders.models import Order,OrderProduct,Payment

# USER ACTIVATION
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

# check password strength
import re,requests
def custom_password_validator(password):
    errors = []
    if len(password) < 8:
        errors.append("Password must be at least 8 characters long.")
    if not re.search(r"[A-Z]", password):
        errors.append("Password must contain at least one uppercase letter.")
    if not re.search(r"[a-z]", password):
        errors.append("Password must contain at least one lowercase letter.")
    if not re.search(r"\d", password):
        errors.append("Password must contain at least one digit.")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        errors.append("Password must contain at least one special character.")
    
    if errors:
        return {'status': 'weak', 'errors': errors}
    return {'status': 'strong', 'errors': []}




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
                
                # check password strength
                result=custom_password_validator(password=password)
                if result['status']=='weak':
                    messages.error(request=request,message=result['errors'][0])
                    return  redirect('register')

                user=Account.objects.create_user(email=email,first_name=first_name,last_name=last_name,username=username,password=password)
                user.phone_number=phone_number
                user.save()
                
                # Default profile
                user_detail=UserDetails()
                user_detail.user=user
                user_detail.profile_picture='default/default.png'
                user_detail.save()

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
            try:
                # load cart if anything added before login
                cart=Cart.objects.get(cart_id=_cart_id(request=request))
                cart_items=CartItem.objects.filter(cart=cart)
                items=CartItem.objects.filter(user=user)
                
                
                cart_variations=[]
                cart_item_id=[]
                for cart_item in cart_items:
                    variation=cart_item.variations.all()
                    cart_variations.append(list(variation))
                    cart_item_id.append(cart_item.id)
                    
                    
                id=[]
                user_variations=[]
                for item in items:
                    variation=item.variations.all()
                    user_variations.append(list(variation))
                    id.append(item.id)
                
                for i,variation in enumerate(cart_variations):
                    if variation in user_variations:
                        index=user_variations.index(variation)
                        item_id=id[index]
                        item=CartItem.objects.get(id=item_id)
                        item.quantity+=1
                        item.user=user
                        item.save()
                    else:
                        cart_item=CartItem.objects.get(id=cart_item_id[i])
                        cart_item.user=user
                        cart_item.save()
                    

            except:
                pass
            auth.login(request=request,user=user)
            url=request.META.get('HTTP_REFERER')
            try:
                query=requests.utils.urlparse(url).query
                params=dict(x.split('=') for x in query.split("&"))
                if 'next' in params:
                    next_page=params['next']
                    return redirect(next_page)
            except:
                pass
            messages.success(request=request,message='Login Successfully!')
            return redirect('dashboard')
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

        # check password strength
        result=custom_password_validator(password=password)
        if result['status']=='weak':
            messages.error(request=request,message=result['errors'][0])
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


# load dashboard
@login_required(login_url='login')
def dashboard(request):
    #find user details for respective user
    user_detail=UserDetails.objects.get(user=request.user)

    # display the count of total orders
    my_orders=OrderProduct.objects.filter(user=request.user,is_ordered=True).order_by('-created_at')
    order_counts=my_orders.count()

    context={
        'order_counts':order_counts,
        'user_detail':user_detail
    }
    return render(request=request,template_name='accounts/dashboard.html',context=context)

@login_required(login_url='login')
def edit_profile(request):

    # find user details
    user_detail=get_object_or_404(UserDetails,user=request.user)
    if request.method=="POST":

        # collect the both user and userProfile form from  post
        # instance is used if any changes then collect that changes
        # request.FILES is for collect the uploaded files if any specified file type then valid accordingly

        user_form=UserForm(request.POST,instance=request.user)
        profile_form=UserProfileForm(request.POST, request.FILES ,instance=user_detail)

        # if valid the save and redirect edit_profile page
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            
            messages.success(request=request,message='Your profile has been updated!')
            return redirect('edit_profile')
    
    # if request method is GET then render with same form to display the data
    user_form=UserForm(instance=request.user)
    profile_form=UserProfileForm(instance=user_detail)
    context={
        'user_form':user_form,
        'profile_form':profile_form,
        'user_detail':user_detail
    }
    return render(request=request,template_name='accounts/edit_profile.html',context=context)

@login_required(login_url='login')
def orders(request):

    # collect all orders for specific user and is_ordered field is True and render orders.html page
    my_orders=OrderProduct.objects.filter(user=request.user,is_ordered=True).order_by('-created_at')
    context={
        'orders':my_orders
    }
    return render(request=request,template_name='accounts/orders.html',context=context)

@login_required(login_url='login')
def change_password(request):

    # logic
    '''
    Few checks such as:-
        newPassword and confirm password should be same
        newPassword should be follow minimum 8 digits with 1 uppercase, 1 lowercase, 1 special charter and 1 numeric value.
        currentPassword should be correct to chnage the newPassword
    '''

    if request.method=='POST':

        currentPassword=request.POST['currentPassword']
        newPassword=request.POST['newPassword']
        confirmPassword=request.POST['confirmPassword']
        if confirmPassword!=newPassword:
            messages.error(request=request,message='Password is not matched with confirm password! ')
            return redirect('change_password')
        result=custom_password_validator(password=newPassword)
        if result['status']=='weak':
            messages.error(request=request,message=result['errors'][0])
            return  redirect('change_password')
        
        user=Account.objects.get(id=request.user.id)
        success=user.check_password(currentPassword)
        if not success:
            messages.error(request=request,message='Please enter valid password!')
            return redirect('change_password')
        user.set_password(newPassword)
        user.save()
        auth.login(request=request,user=user)
        messages.success(request=request,message='Password changed successfully!')
        return redirect('change_password')
    return render(request=request,template_name='accounts/change_password.html')