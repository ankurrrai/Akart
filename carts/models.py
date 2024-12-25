from django.db import models
from store.models import Product
from django.urls import reverse

class Cart(models.Model):
    cart_id=models.CharField(max_length=250,blank=True)
    date_added=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

class CartItem(models.Model):

    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,null=True)
    is_active=models.BooleanField(default=True)
    quantity=models.IntegerField()

    def sub_total(self):
        return self.quantity*self.product.price
    
    

    def __str__(self):
        return self.product.product_name