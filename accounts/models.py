from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password =None):
        """
        Creates and saves a User with the given  first_name, last_name, username, and email.
        """
        
        if not email:
            raise ValueError('User must have an email address')
        
        if not username:
            raise ValueError('User must have a username')
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )
        
        user.set_password(password)
        # user.is_active = True
        user.save(using=self._db)
        

        return user
    
    def create_superuser(self, first_name, last_name, username, email, password =None):
        """
        Creates and saves a superser with the given  first_name, last_name, username, and email.
        """
        
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
        )
        
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user
    
    
class User(AbstractBaseUser):
    WATER_SUPPLIER = 1
    CUSTOMER = 2 
    
    ROLE_CHOICE = (
        (WATER_SUPPLIER, 'Supplier'),
        (CUSTOMER, 'Customer'),
    )
    
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    username = models.CharField(max_length=45, unique=True)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    # phone_number = PhoneNumberField(blank=True, unique=True)
    phone_number = models.CharField(max_length=10, blank=True)
    role = models.PositiveSmallIntegerField(choices = ROLE_CHOICE, blank=True, null=True)
    
    
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS =  ['username', 'first_name', 'last_name']
    
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        "Return True if the user is an active super user or is an admin"
        return True
    
    """
    Detect the type of user and send them to their respective dashboard
    """
    def get_role(self):
        if self.role == 1:
            user_role = 'Supplier'
        if self.role == 2:
            user_role = 'Customer'
        return user_role
    
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='users/profile_pictures', blank=True, null=True)
    cover_photo = models.ImageField(upload_to='users/cover_photos', blank=True, null=True) 
    country = CountryField(blank_label='(select country)')
    county = models.CharField(max_length=15, blank=True, null=True)
    town = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    pin_code = models.CharField(max_length=6, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.user.email