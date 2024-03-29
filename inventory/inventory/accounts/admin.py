from django.contrib import admin
from django.contrib.auth import get_user_model

from inventory.accounts.models import Profile

UserModel = get_user_model()


@admin.register(UserModel)
class AppUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'date_joined', 'last_login', 'is_staff', 'is_superuser',)
    list_filter = ('is_staff', 'is_superuser',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            'Permissions',
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                ),
            },
        ),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    ordering = ('-date_joined',)
    search_fields = ('email',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number')
    ordering = ('first_name', 'last_name',)
    search_fields = ('first_name', 'last_name', 'phone_number',)
