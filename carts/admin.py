from django.contrib import admin
from .models import *

# register the Cart and CartItem Model
class cartItemAdmin(admin.ModelAdmin):
    list_display=['product','quantity','is_active']


admin.site.register(Cart)
admin.site.register(CartItem,cartItemAdmin)
