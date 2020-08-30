from django.shortcuts import render, redirect
from .forms import LoginForm, VerifyTokenForm, SignUpForm
from django.views import View
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.views import LogoutView 
import phone_send.settings as setting
import hashlib
import os
from .phoneBackend import PhoneBackend
from .message import send_message
from .models import LoginAuthenticate
from datetime import datetime
from django.utils import timezone


class LoginIn(View):

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        context = {
            'form': form,
            'title': "Вход"
        }
        return render(request, 'accounts/login.html', context)

    def post(self, request, *args, **kwargs): 
        form = LoginForm(request.POST) 
        if form.is_valid():
            cd = form.cleaned_data 
            request.session['phone'] = cd['phone']
              
            hash_algorithm = getattr(setting, 'PHONE_LOGIN_OTP_HASH_ALGORITHM', 'sha256')
            m = getattr(hashlib, hash_algorithm)()
            m.update(getattr(setting, 'SECRET_KEY', None).encode('utf-8'))
            m.update(os.urandom(16))
            code = str(int(m.hexdigest(), 16))[-6:]   
            ob = LoginAuthenticate.objects.filter(phone=cd['phone'], code='') 
            if len(ob) == 0:
                login = LoginAuthenticate.objects.create()
                login.phone = cd['phone']
                login.code = code
                login.begin_time =timezone.now()
                login.save()
            body = 'wow ' + str(code) 
            send_message(str(cd['phone']), body)
            return redirect('success')  


class SignOutView(LogoutView):
    next_page = '/'


class VerifySuccess(View):

    def get(self, request, *args, **kwargs):
        form = VerifyTokenForm()
        phone = request.session.get('phone') 
        otp = request.session.get('otp')
        context = {
            'form': form,
            'title': "Вход",
            'error': 'На ваш телефон ' + str(phone) + ' отправлен код',
        }  

        return render(request, 'accounts/login_token.html', context)

    def post(self, request, *args, **kwargs):
        form = VerifyTokenForm(request.POST)
        if form.is_valid(): 
            phone = request.session.get('phone')  
            cd = form.cleaned_data 
            res = cd['code'] 
            ob = LoginAuthenticate.objects.filter(phone=phone, code=res)
            if not len(ob) == 0: 
                login = ob[0] 
                difference = timezone.now() - login.begin_time 
                if difference.seconds <= 60:
                    login.success = True
                    login.save()
                    ph_back = PhoneBackend()
                    user = ph_back.authenticate(phone=phone)
                    if user is not None:
                        if user.is_active:
                            user.save() 
                            auth_login(request, user) 
                            return redirect('home')
                    else:
                        form = LoginForm()
                        context = { 
                            'error': 'Не верный логин',
                            'title': "Вход",
                            'form': form
                        }
                else:
                    form = LoginForm()
                    context = { 
                        'error': 'Время вышло',
                        'title': "Вход",
                        'form': form
                    }
            else:
                form = LoginForm()
                context = { 
                        'error': 'Не верный логин или код',
                        'title': "Вход",
                        'form': form
                    }
            return render(request, 'accounts/login_token.html', context)

class SignUp(View):

    def get(self, request, *args, **kwargs):
        form = SignUpForm()
        context = {
            'form': form,
            'title': "Регистрация"
        }
        return render(request, 'accounts/signup.html', context)

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid():  
            user = form.save()    
            return redirect("login")
        else:
            error = form.errors.as_json()
            form = SignUpForm() 
            context = {
                'form': form,
                'error': error,
                'title': "Регистрация"
            }
            return render(request, 'accounts/signup.html', context)