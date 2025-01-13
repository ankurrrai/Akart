from django.shortcuts import render,redirect
from carts.models import CartItem
from store.models import Product
from .models import Order,Payment,OrderProduct
from .forms import OrderForm
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,JsonResponse


import json,time,string,random


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
    return f"{timestamp}{random_str}"


@login_required(login_url='login')
def payments(request):

    # collect body from client side i.e via fetch
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

    # move the carts item to Order product table
    cart_items=CartItem.objects.filter(user=request.user)
    for item in cart_items:
        orderProduct=OrderProduct()
        orderProduct.order=order
        orderProduct.payment=payment
        orderProduct.user=request.user
        orderProduct.product=item.product
        orderProduct.quantity=item.quantity
        orderProduct.product_price=item.product.price
        orderProduct.is_ordered=True
        orderProduct.save()

        cart_item=CartItem.objects.get(id=item.id)
        orderProduct=OrderProduct.objects.get(id=orderProduct.id)
        orderProduct.variation.set(cart_item.variations.all())
        orderProduct.save()
        
        #reduce the qunatity if the sold product    
        product=Product.objects.get(id=item.product.id)
        product.stock-=item.quantity
        product.save()

    #clear the cart
    CartItem.objects.filter(user=request.user).delete()
    
    #send confirmation email to customer
    subject_name='AKART | Order Confirmation!'
    message=render_to_string(template_name='orders/order_confirmation.html',context={
        'order':order,
        'user':request.user,
        
    })
    send_email=EmailMessage(subject=subject_name,body=message,to=[order.email,order.user.email])
    send_email.send()

    #send response to client
    data={

        'orderId':order.order_number,
        'paymentId':payment.payment_id,
    }

    return JsonResponse(data=data)

    


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
    
@login_required(login_url='login')
def order_complete(request):
    try:
        orderId=request.GET.get('orderId')
        paymentId=request.GET.get('paymentId')
        displaySuccess=True
        try:
            if request.GET.get('displaySuccess')=='false':
                displaySuccess=False
        except:
            pass

        order=Order.objects.get(order_number=orderId,user=request.user)
        payment=Payment.objects.get(payment_id=paymentId,user=request.user)
        order_products=OrderProduct.objects.filter(order=order,payment=payment,user=request.user)
        
        sub_total=0
        for item in order_products:
            sub_total+=item.product_price*item.quantity

        context={
            'order_products':order_products,
            'order':order,
            'payment':payment,
            'sub_total':sub_total,
            'displaySuccess':displaySuccess
        }
        return render(request=request,template_name='orders/order_complete.html',context=context)
    except (Payment.DoesNotExist,Order.DoesNotExist):
        return redirect('home')
    

 