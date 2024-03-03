from django.urls import path, include

from inventory.business.views import CreateBusinessView, BusinessView
from inventory.devices.views import DeviceCreateView

urlpatterns = (
    path('<int:pk>/', BusinessView.as_view(), name='business'),
    path('<int:business_id>/device/create/', DeviceCreateView.as_view(), name='create-device'),
    path('create/', CreateBusinessView.as_view(), name='create-business'),
)
