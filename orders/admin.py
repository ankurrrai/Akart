from django.contrib import admin
from .models import Payment,Order,OrderProduct

class OrderProductInline(admin.TabularInline):
    model=OrderProduct
    readonly_fields=['payment','order','user','product','variation','product_price','quantity','is_ordered']
    can_delete=False
    extra=0

class OrderAdmin(admin.ModelAdmin):
    list_display=['first_name','email','user','payment','order_number','status','is_ordered','created_at']
    list_display_links=['first_name','email','user','payment','order_number']
    list_filter=['first_name','email','user','payment','order_number','status','is_ordered','created_at']
    # search_fields=['first_name','email','user','payment','order_number']
    list_per_page=20
    inlines=[OrderProductInline]

admin.site.register(Payment)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderProduct)
