from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('inventory.common.urls')),
    path('auth/', include('inventory.accounts.urls')),
    path('business/', include('inventory.business.urls')),
    path('supplier/', include('inventory.suppliers.urls')),
]
