from inventory import settings
from django.contrib import admin
from django.core.mail import send_mail
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include('inventory.common.urls')),
                  path('auth/', include('inventory.accounts.urls')),
                  path('business/', include('inventory.business.urls')),
                  path('supplier/', include('inventory.suppliers.urls')),
                  path('device/', include('inventory.devices.urls')),
                  path('organization/', include('inventory.organization.urls')),
                  path('report/', include('inventory.reports.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# send_mail(
#     subject='It works!',
#     message='It works without HTML!',
#     from_email=settings.EMAIL_HOST_USER,
#     recipient_list=['tonytech1983@gmail.com'],
#     fail_silently=False,
#     auth_user=None,
#     auth_password=None,
#     connection=None,
#     html_message=None,
# )
