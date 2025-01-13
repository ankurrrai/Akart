from django.db import models
from category.models import Category
from django.urls import reverse
from accounts.models import Account
from django.db.models import Avg,Count

class Product(models.Model):
    
    product_name=models.CharField(max_length=250,unique=True)
    slug=models.SlugField(max_length=250,unique=True)
    description=models.TextField(max_length=1000,blank=True)
    price=models.IntegerField()
    product_image=models.ImageField(upload_to='photos/product',blank=True)
    stock=models.IntegerField()
    is_available=models.BooleanField(default=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    created_date=models.DateTimeField(auto_now_add=True)
    modified_date=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name
    
    def average_rating(self):
        review=RatingReview.objects.filter(product=self,status=True).aggregate(average=Avg('rating'))
        avg=0
        if review['average'] is not None:
            avg=float(review['average'])
        return avg
    def count_of_ratings(self):
        review=RatingReview.objects.filter(product=self,status=True).aggregate(count=Count('id'))
        count=0
        if review['count'] is not None:
            count=int(review['count'])
        return count

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
    
class RatingReview(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user=models.ForeignKey(Account,on_delete=models.CASCADE)
    rating=models.FloatField()
    subject=models.CharField(max_length=150)
    review=models.TextField(max_length=500)
    status=models.BooleanField(default=True)
    ip=models.CharField(max_length=100,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject
    

class ProductGallery(models.Model):
    product=models.ForeignKey(Product,default=None,on_delete=models.CASCADE)
    image=models.ImageField(max_length=255,upload_to='store/products')

    class Meta:
        verbose_name='Product Gallery'
        verbose_name_plural='Product Galleries'

    def __str__(self):
        return self.product.product_name