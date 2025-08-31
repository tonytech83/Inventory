from django.conf.urls.static import static
from django.contrib import admin
from django.core.mail import send_mail
from django.urls import include, path

from inventory import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("inventory.common.urls")),
    path("auth/", include("inventory.accounts.urls")),
    path("business/", include("inventory.business.urls")),
    path("supplier/", include("inventory.suppliers.urls")),
    path("device/", include("inventory.devices.urls")),
    path("organization/", include("inventory.organization.urls")),
    path("report/", include("inventory.reports.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
