from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'first_name', 'last_name', 'is_active', ]
    search_fields = ['email', 'first_name', 'last_name', ]
    ordering = ['email', ]
    

admin.site.register(CustomUser, CustomUserAdmin)