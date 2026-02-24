from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser, Permission, Resource, Role


# Register your models here.
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = ['email', 'first_name', 'last_name', 'role', 'is_active', ]
    search_fields = ['email', 'first_name', 'last_name', ]
    ordering = ['email', ]

    fieldsets = [
        (None, {'fields': ('email', 'password')}),
        (('Personal info'), {'fields': ('first_name', 'middle_name', 'last_name', 'role')}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (('Important dates'), {'fields': ('last_login',)}),
    ]

    # change field password to psw1, psw2
    fieldsets[0][-1]['fields'] = ('email', 'password1', 'password2')
    add_fieldsets = fieldsets
    

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Role)
admin.site.register(Resource)
admin.site.register(Permission)