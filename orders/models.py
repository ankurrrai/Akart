from django.db import models

from accounts.models import Account
from store.models import Product,Variation


# Keep the details payment details
class Payment(models.Model):
    user=models.ForeignKey(Account,on_delete=models.CASCADE)
    payment_id=models.CharField(max_length=100)
    payment_method=models.CharField(max_length=100)
    amount_paid=models.CharField(max_length=100)
    status=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.payment_id
    

# All order details
class Order(models.Model):
    STATUS=[['Accepted','Accepted'],['Dispatched','Dispatched'] ,['Delivered','Delivered'],['Cancelled','Cancelled']]

    user=models.ForeignKey(Account,on_delete=models.SET_NULL,null=True)
    payment=models.ForeignKey(Payment,on_delete=models.SET_NULL,blank=True,null=True)
    order_number=models.CharField(max_length=40)
    first_name=models.CharField(max_length=40)
    last_name=models.CharField(max_length=40)
    phone_number=models.CharField(max_length=15)
    email=models.EmailField(max_length=50)
    address_line_1=models.CharField(max_length=100)
    address_line_2=models.CharField(max_length=100,blank=True)
    country=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    pin_code=models.CharField(max_length=50)
    order_note=models.CharField(max_length=200,blank=True)
    order_total=models.FloatField()
    tax=models.FloatField()
    status=models.CharField(max_length=100,choices=STATUS,default='Accepted')
    ip=models.CharField(blank=True,max_length=20)
    is_ordered=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def full_name(self):
        return f"{self.first_name.capitalize()} {self.last_name.capitalize()}"
    
    def address(self):
        return f"{self.address_line_1}, {self.address_line_2}"
    
    def zipCode(self):
        return f"{self.state}, {self.country}-{self.pin_code}"
    
    def contactDetails(self):
        return f"Email: {self.email}, Phone Number: {self.phone_number}"

    def __str__(self):
        return self.order_number

# Keep the cart prdouct here along with user,order and payment 
class OrderProduct(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    payment=models.ForeignKey(Payment,on_delete=models.SET_NULL,blank=True,null=True)
    user=models.ForeignKey(Account,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    variation=models.ManyToManyField(Variation,blank=True)
    quantity=models.IntegerField()
    product_price=models.FloatField()
    is_ordered=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def sub_total(self):
        return self.product_price*self.quantity

    def __str__(self):
        return self.product.product_name