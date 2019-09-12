from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User
from .forms import UserAdminCreationForm, UserAdminForm, UserMultiForm


# Register your models here.
class UserAdmin(BaseUserAdmin):

    add_form = UserMultiForm
    add_fieldsets = (
        (None, {
            'fields': ('username', 'email', 'password1', 'password2')
        }),
    )
    form = UserAdminForm
    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'people', 'profile_picture')
        }),
        (
            'Permissões', {
                'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'
                )
            }
        ),
    )
    list_display = ['username', 'people', 'email', 'is_active', 'is_staff']

admin.site.register(User, UserAdmin)