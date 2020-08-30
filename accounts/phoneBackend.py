from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from .models import Profile

class PhoneBackend(ModelBackend):
    def __init__(self, *args, **kwargs):
        self.user_model = get_user_model()

    
    def authenticate(self, phone=None, password=None, **extra_fields):
        if phone is None:
            return 
        print(phone)
        try: 
            profile = Profile.objects.get_user(phone=extra_fields.get('username'))
        except Profile.DoesNotExist:  
            raise Profile.DoesNotExist 
        return profile