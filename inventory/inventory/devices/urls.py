from django.urls import path

from inventory.devices.views import DeviceDeleteApiView, download_template, DeviceUpdateApiView

urlpatterns = (
    path('edit/<int:pk>/', DeviceUpdateApiView.as_view(), name='edit-device'),
    path('delete/<int:pk>/', DeviceDeleteApiView.as_view(), name='delete-device'),
    path('download-template/', download_template, name='download-template'),
)
