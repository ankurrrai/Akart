from django.contrib import admin
from .models import Account,UserDetails
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

class UserDetailsAdmin(admin.ModelAdmin):
    def thumbnail(self,object):
        return format_html('<img src="{}" width="30" style="border-radius=50%;">'.format(object.profile_picture.url))
    thumbnail.short_description='profile_picture'

    list_display=['thumbnail','user','pin_code','country','state']
    list_display_links=['thumbnail','user','pin_code','country','state']
    

class AccountAdmin(UserAdmin):
    list_display=['email','username','first_name','last_name','date_joined','last_login','is_active']
    list_display_links=['email','username']
    ordering=['-date_joined']
    readonly_fields=['date_joined','last_login']

    filter_horizontal=[]
    list_filter=[]
    fieldsets=[]

admin.site.register(Account,AccountAdmin)
admin.site.register(UserDetails,UserDetailsAdmin)