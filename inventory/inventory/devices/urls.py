from django.urls import path

from inventory.devices.views import DeviceCreateView, DeviceEditView, DeviceDeleteView, CSVUploadView

urlpatterns = (
    path('edit/<int:pk>/', DeviceEditView.as_view(), name='edit-device'),
    path('delete/<int:pk>/', DeviceDeleteView.as_view(), name='delete-device'),
    path('upload-csv/', CSVUploadView.as_view(), name='upload-csv'),
)
