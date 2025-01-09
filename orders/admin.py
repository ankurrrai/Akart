from django.contrib import admin
from .models import Payment,Order,OrderProduct


class OrderAdmin(admin.ModelAdmin):
    list_display=['first_name','email','user','payment','order_number','status','is_ordered','created_at']
    list_display_links=['first_name','email','user','payment','order_number']
    list_filter=['first_name','email','user','payment','order_number','status','is_ordered','created_at']

admin.site.register(Payment)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderProduct)
