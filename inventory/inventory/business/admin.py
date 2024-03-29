from django.contrib import admin

from inventory.business.models import Business


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    fields = ('business_name', 'country', 'is_visible', 'owner')
    list_display = ('business_name', 'country', 'is_visible', 'owner')
    list_filter = ('country', 'is_visible', 'owner')

