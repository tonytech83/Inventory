from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

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
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
