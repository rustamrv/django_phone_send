from django import forms 
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class LoginForm(forms.Form):
    phone = forms.CharField()

class VerifyTokenForm(forms.Form):
    code = forms.CharField()

class SignUpForm(UserCreationForm): 

    class Meta:
        model = Profile
        fields = ('phone', 'fullname', 'password1', 'password2')
 