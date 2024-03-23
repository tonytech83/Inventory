from django.urls import path

from inventory.business.views import BusinessView, EditBusinessView, CreateBusinessApiView
from inventory.devices.views import DeviceCreateAPIView, CSVUploadApiView

urlpatterns = (
    path('<int:pk>/', BusinessView.as_view(), name='business'),
    path('create/', CreateBusinessApiView.as_view(), name='create-business'),
    path('edit/<int:pk>/', EditBusinessView.as_view(), name='edit-business'),

    path('<int:business_id>/device/create/', DeviceCreateAPIView.as_view(), name='create-device'),
    path('<int:business_id>/upload-csv/', CSVUploadApiView.as_view(), name='upload-csv'),
)
