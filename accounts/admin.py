from django.contrib import admin
from .models import Profile, LoginAuthenticate
 
@admin.register(Profile)
class ProdileAdmin(admin.ModelAdmin):
    list_display = ('phone', 'fullname', )

@admin.register(LoginAuthenticate)
class LoginAdmin(admin.ModelAdmin):
    list_display = ('phone', 'code', 'success', )