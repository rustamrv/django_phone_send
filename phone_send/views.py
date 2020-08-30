from django.shortcuts import render, redirect 
from django.views import View

class HomePage(View):

    def get(self, request, *args, **kwargs): 
        context = { 
            
        }
        return render(request, 'layout/home.html', context)