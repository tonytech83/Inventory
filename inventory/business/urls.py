from django.urls import path

from inventory.business.views import (
    BusinessView,
    CreateBusinessApiView,
    UpdateBusinessApiView,
)
from inventory.devices.views import CSVUploadApiView, DeviceCreateAPIView

urlpatterns = (
    path("<int:pk>/", BusinessView.as_view(), name="business"),
    path("create/", CreateBusinessApiView.as_view(), name="create-business"),
    path("edit/<int:pk>/", UpdateBusinessApiView.as_view(), name="edit-business"),
    path(
        "<int:business_id>/device/create/",
        DeviceCreateAPIView.as_view(),
        name="create-device",
    ),
    path(
        "<int:business_id>/upload-csv/",
        CSVUploadApiView.as_view(),
        name="upload-csv",
    ),
)
