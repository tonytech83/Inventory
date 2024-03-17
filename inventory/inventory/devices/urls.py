from django.urls import path

from inventory.devices.views import DeviceEditView, DeviceDeleteView, download_template

urlpatterns = (
    path('edit/<int:pk>/', DeviceEditView.as_view(), name='edit-device'),
    path('delete/<int:pk>/', DeviceDeleteView.as_view(), name='delete-device'),
    path('download-template/', download_template, name='download-template'),
)
