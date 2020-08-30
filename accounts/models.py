from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin


class PhoneNumberUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, phone_number,
                     password, **extra_fields):
        """
        Creates and saves a User with the given phone_number and password.
        """  
        user = self.model(phone=phone_number,
            **extra_fields
        )
        user.set_password(password) 
        user.save(using=self._db)
        return user

    def get_user(self, phone, **extra_fields):
        user = self.model(phone=phone,  
                        **extra_fields
                            ) 
        return user

    def create_user(self, phone_number=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone_number, password,
                                 **extra_fields)

    def create_superuser(self, phone, password,
                         **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True) 
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone, password,
                                 **extra_fields)

class Profile(AbstractBaseUser, PermissionsMixin):
    phone = PhoneNumberField(unique=True, primary_key=True)
    fullname = models.CharField(max_length=255, default="Test") 
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone' 

    objects = PhoneNumberUserManager()

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        return self.fullname 
  


class LoginAuthenticate(models.Model):
    phone = models.CharField(max_length=20)
    code = models.CharField(max_length=10)
    begin_time = models.DateTimeField(auto_now=True)
    success = models.BooleanField(default=False) 

    def __str__(self):
        return self.code