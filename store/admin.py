from django.contrib import admin
from .models import Product,Variation,RatingReview

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields={
        'slug':['product_name']
    }

    list_display=['product_name','slug','price','stock','category','modified_date','is_available']
    list_display_links=['product_name','slug']

class VariationAdmin(admin.ModelAdmin):
    list_display=['product','variation_category','variation_value','is_active']
    list_filter=['product','variation_category','variation_value','is_active']

admin.site.register(Product,ProductAdmin)
admin.site.register(Variation,VariationAdmin)
admin.site.register(RatingReview)

