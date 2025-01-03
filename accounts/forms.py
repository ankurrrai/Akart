from django import forms
from .models import Account

class RegisterForm(forms.ModelForm):
    class Meta:
        model= Account
        fields=['first_name','last_name','phone_number','email','password']