from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields={
        'slug':['product_name']
    }

    list_display=['product_name','slug','price','stock','category','modified_date','is_available']
    list_display_links=['product_name','slug']

admin.site.register(Product,ProductAdmin)

