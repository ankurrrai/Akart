from django.shortcuts import render,redirect
from carts.models import CartItem
from .models import Order,Payment
from .forms import OrderForm
from django.contrib.auth.decorators import login_required
import time,string,random

from django.http import HttpResponse
import json

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # Get the first IP in the list
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def generate_order_number():
    timestamp = int(time.time())  # Current timestamp
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"{timestamp}_{random_str}_"


@login_required(login_url='login')
def payments(request):

    body=request.body
    details=json.loads(body)

    order=Order.objects.get(order_number=details['orderID'])
    payment=Payment()
    payment.payment_id=details['tarnscationID']
    payment.status=details['status']
    payment.payment_method=details['payment_method']
    payment.amount_paid=order.order_total
    payment.user=request.user

    payment.save()

    order.payment=payment
    order.is_ordered=True
    order.save()


    return redirect('dashboard')


@login_required(login_url='login')
def place_order(request,total=0,quantity=0,cart_items=None,grand_total=0,tax=0):
    current_user=request.user
    cart_items=CartItem.objects.filter(user=current_user)
    carts_count=cart_items.count()

    if carts_count <=0:
        return redirect('cart')
    
    for cart_item in cart_items:
        total+=cart_item.product.price*cart_item.quantity
        quantity+=cart_item.quantity
    
    tax=(2*total)/100
    grand_total=total+tax

    if request.method=='POST':
        
        form=OrderForm(request.POST)
        is_form_valid=form.is_valid()
        if is_form_valid:
            order=Order()
            order.user=current_user
            order.first_name=form.cleaned_data['first_name']
            order.last_name=form.cleaned_data['last_name']
            order.phone_number=form.cleaned_data['phone_number']
            order.email=form.cleaned_data['email']
            order.address_line_1=form.cleaned_data['address_line_1']
            order.address_line_2=form.cleaned_data['address_line_2']
            order.country=form.cleaned_data['country']
            order.state=form.cleaned_data['state']
            order.pin_code=form.cleaned_data['pin_code']
            order.order_note=form.cleaned_data['order_note']

            order.order_total=grand_total
            order.tax=tax
            order.ip=get_client_ip(request=request)
            order.save()
            
            order_number=generate_order_number() + str(order.id)
            order.order_number=order_number
            order.save()

            order=Order.objects.get(order_number=order_number,is_ordered=False,user=current_user)
            context={
                'order':order,
                'cart_items':cart_items,
                'total':total,
                'grand_total':grand_total,
                'tax':tax,
               
            }

            return render(request=request,template_name='orders/payments.html',context=context)
        else:
            return redirect('cart')
    else:
        return redirect('checkout')


