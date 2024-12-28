from django.db import models
from category.models import Category
from django.urls import reverse


class Product(models.Model):
    
    product_name=models.CharField(max_length=250,unique=True)
    slug=models.SlugField(max_length=250,unique=True)
    description=models.TextField(max_length=1000,blank=True)
    price=models.IntegerField()
    product_image=models.ImageField(upload_to='photos/product',blank=True)
    stock=models.IntegerField()
    is_available=models.BooleanField(default=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    created_date=models.DateTimeField(auto_now=True)
    modified_date=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name
    
    def get_url(self):
        return reverse(viewname='product_details',args=[self.category.slug,self.slug])

# varition class has to define to change the category and value for different parameters 
class VaraitionManager(models.Manager):
    def colors(self):
        return super(VaraitionManager,self).filter(variation_category='color',is_active=True)
    def sizes(self):
        return super(VaraitionManager,self).filter(variation_category='size',is_active=True)


variation_choices=[
    ['color','color'],['size','size']
]

class Variation(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)  #by default related-name is  class name is taking
    variation_category=models.CharField(max_length=250,choices=variation_choices)
    variation_value=models.CharField(max_length=250,blank=False)
    is_active=models.BooleanField(default=True)
    created_date=models.DateTimeField(auto_now=True)

    objects=VaraitionManager()

    def __str__(self):
        return self.variation_value
