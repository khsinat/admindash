from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Custom User Manager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Create and return a user with an email and password"""
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser with an email and password"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_verified', True)  # Ensure is_verified is set if needed

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)
# Custom User Model
class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    full_name = models.CharField(max_length=510, null=True, blank=True)
    password = models.CharField(max_length=255)
    state_id = models.IntegerField(null=True, blank=True)
    contact_no = models.CharField(max_length=15, null=True, blank=True)
    fcm_token = models.CharField(max_length=255, null=True, blank=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    profile_file = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)

    # Custom manager
    objects = UserManager()

    # Fields required by Django's user creation process
    REQUIRED_FIELDS = ['first_name', 'last_name']  # Fields required when creating a user (except for email and password)
    
    # Specify the field used for login (email in this case)
    USERNAME_FIELD = 'email'
