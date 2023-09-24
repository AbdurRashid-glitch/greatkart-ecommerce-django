from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.


class MyAccountmanager(BaseUserManager):
    # to create a user:
    def create_user(self, username, first_name, last_name, email, password=None):
        if not email:
            raise ValueError('Please provide an email address')
        
        if not username:
            raise ValueError('User must have an username')
        
        user = self.model(
            email = self.normalize_email(email), # every letter of email will be normalized(small letter)
            username = username,
            first_name = first_name,
            last_name = last_name,
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, first_name, last_name, email, password):
        # now using the above 'create_user' method inside of this superuser method:
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name= last_name,
        )
        
        # as Superuser we have to set all the permissions to true:
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=30)
    
    #Required:
    
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email' # can be able to login with an email address
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    # We need to tell this account that we are using MyAccountManager for all the operations
    objects = MyAccountmanager()
    
    def __str__(self):
        return self.email
    
    # if the user is admin then he has the authority to change
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, add_label):
        return True
    