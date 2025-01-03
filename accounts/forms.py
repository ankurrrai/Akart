from django import forms
from .models import Account

class RegisterForm(forms.ModelForm):

    password=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}))
    confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password'}))
    email   =forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'abc@xyz.com','type':'email'}))
    phone_number=forms.Field(widget=forms.NumberInput(attrs={'placeholder':'+91-123 123 1234'}))
    
    class Meta:
        model= Account
        fields=['first_name','last_name','phone_number','email','password']

    def clean(self):
        
        cleaned_data= super(RegisterForm,self).clean()
        password=cleaned_data.get('password')
        confirm_password=cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Password doest not match!')

    def __init__(self,*args,**kwargs):
        super(RegisterForm,self).__init__(*args,**kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'
            self.fields[field].widget.attrs['placeholder']=field.replace('_',' ').capitalize()

    