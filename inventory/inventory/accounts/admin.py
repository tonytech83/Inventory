from django.contrib import admin

from inventory.accounts.models import AppUser


@admin.register(AppUser)
class AppUserAdmin(admin.ModelAdmin):
    pass
