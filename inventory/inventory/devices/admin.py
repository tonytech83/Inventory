from django.contrib import admin

from inventory.devices.models import Device


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('device_name', 'status', 'model', 'category', 'serial_number', 'eos')
    list_filter = ('status', 'business', 'category', 'sub_category', 'supplier')

    fieldsets = (
        ('Device', {'fields': (
            'device_name', 'domain', 'description', 'status', 'category', 'sub_category',
            'manufacturer', 'model', 'ip_address', 'ip_address_sec', 'serial_number', 'operating_system',
            'building', 'owner_name')}),
        ('Support', {'fields': (
            'support_model', 'purchase_order_number', 'invoice_img', 'sos', 'eos', 'eol',
        )}),
        ('Risk', {'fields': (
            'business_processes_at_risk', 'impact', 'likelihood',
        )}),
        ('Supplier', {'fields': ('supplier',)}),
        ('Business', {'fields': ('business',)})
    )
