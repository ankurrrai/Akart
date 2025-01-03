from django.db import models
from store.models import Product,Variation
from django.urls import reverse

#  Cart is baiscally used to store the session_key
class Cart(models.Model):
    cart_id=models.CharField(max_length=250,blank=True)
    date_added=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

class CartItem(models.Model):

    # add require fields 
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,null=True)
    variations=models.ManyToManyField(Variation,blank=True,null=True)
    is_active=models.BooleanField(default=True)
    quantity=models.IntegerField()

    
    # this function is used to calculate the total based on quantity
    def sub_total(self):
        return self.quantity*self.product.price
    
    
    # This is for display to admin pannel
    def __str__(self):
        return self.product.product_name