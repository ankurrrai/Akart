from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager


class MyAccountManager(BaseUserManager):
    # this for adding user
    def create_user(self,first_name,last_name,username,email,password=None):
        user=self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    # call to add create superuser
    def create_superuser(self,first_name,last_name,username,email,password=None):
        user=self.create_user(first_name=first_name,last_name=last_name,email=email,password=password,username=username)
        user.is_admin=True
        user.is_staff=True
        user.is_active=True
        user.is_superadmin=True

        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    username=models.CharField(max_length=50,unique=True)
    email=models.EmailField(max_length=100,unique=True)
    phone_number=models.CharField(max_length=50)

    # required
    date_joined=models.DateTimeField(auto_now=True)
    last_login=models.DateTimeField(auto_now=True)
    is_admin=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    is_active=models.BooleanField(default=False)
    is_superadmin=models.BooleanField(default=False)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username','first_name','last_name']

    objects=MyAccountManager()

    def profile_picture_url(self):
        user_details=UserDetails.objects.get(user=self)
        return user_details.profile_picture.url

    def __str__(self):
        return self.email
    
    def has_perm(self,perm,obj=None):
        return self.is_admin
    
    def has_module_perms(self,add_label):
        return True

# User details for keep user profile picture and other personal details
class UserDetails(models.Model):
    user=models.OneToOneField(Account,on_delete=models.CASCADE)
    profile_picture=models.ImageField(upload_to='user/profile_picture')
    address_line_1=models.CharField(max_length=150,blank=True)
    address_line_2=models.CharField(max_length=150,blank=True)
    country=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    pin_code=models.CharField(max_length=50)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    
    def address(self):
        return f"{self.address_line_1}, {self.address_line_2}"
    
    def zipCode(self):
        return f"{self.state}, {self.country}-{self.pin_code}"
    
    def contactDetails(self):
        return f"Email: {self.email}, Phone Number: {self.phone_number}"
    
    def __str__(self):
        return self.user.email