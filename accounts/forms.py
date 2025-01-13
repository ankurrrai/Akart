from django import forms
from .models import Account,UserDetails

class RegisterForm(forms.ModelForm):

    password=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}))
    confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password'}))
    email   =forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'abc@xyz.com','type':'email'}))
    # phone_number=forms.CharField(widget=forms.(attrs={'placeholder':'+91-123 123 1234'}))
    
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

class UserForm(forms.ModelForm):
    class Meta:
        model= Account
        fields=['first_name','last_name','phone_number','email']
    
    def __init__(self,*args,**kwargs):
        super(UserForm,self).__init__(*args,**kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'


class UserProfileForm(forms.ModelForm):
    profile_picture=forms.ImageField(required=False,error_messages={'invalid':("Image files only")},widget=forms.FileInput)
    class Meta:
        model= UserDetails
        fields=['profile_picture','address_line_1','address_line_2','country','state','pin_code']
    
    def __init__(self,*args,**kwargs):
        super(UserProfileForm,self).__init__(*args,**kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'
    