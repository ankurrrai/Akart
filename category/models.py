from django.db import models
from django.urls import reverse

# Category model
class Category(models.Model):
    category_name=models.CharField(max_length=50,unique=True)
    slug=models.SlugField(max_length=100,unique=True)
    description=models.TextField(max_length=300,blank=True)
    cat_image=models.ImageField(upload_to='photos/categories',blank=True)

    # META class have used here for name pural name which will reflect to admin pannel
    class Meta:
        verbose_name='category'
        verbose_name_plural='categories'
    
    # get the product_by_category url
    def get_url(self):
        return reverse(viewname='product_by_category',args=[self.slug])
    
    def __str__(self):
        return self.category_name
