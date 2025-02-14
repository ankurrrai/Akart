from django import forms
from .models import Order

# Order form
class OrderForm(forms.ModelForm):

    class Meta:
        model=Order
        fields=['first_name','last_name','phone_number','email','address_line_1','address_line_2','country','state','pin_code','order_note']