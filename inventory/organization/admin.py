from django.contrib import admin

from inventory.organization.models import Organization


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = (
        "organization_name",
        "region",
    )
