from django.contrib import admin
from django.urls import path, include

from inventory.accounts.views import custom_permission_denied_view

# Custom permission denied handler
handler403 = custom_permission_denied_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('inventory.common.urls')),
    path('auth/', include('inventory.accounts.urls')),
    path('business/', include('inventory.business.urls')),
    path('supplier/', include('inventory.suppliers.urls')),
    path('device/', include('inventory.devices.urls')),
]
