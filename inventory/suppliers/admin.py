from django.contrib import admin

from inventory.suppliers.models import Supplier


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "contact_name",
        "supplier_country",
        "phone_number",
        "email",
    )
    list_filter = ("supplier_country",)
