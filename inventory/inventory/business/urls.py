from django.urls import path

from inventory.business.views import CreateBusinessView, BusinessView, EditBusinessView
from inventory.devices.views import DeviceCreateView

urlpatterns = (
    path('<int:pk>/', BusinessView.as_view(), name='business'),
    path('create/', CreateBusinessView.as_view(), name='create-business'),
    path('edit/<int:pk>/', EditBusinessView.as_view(), name='edit-business'),

    path('<int:business_id>/device/create/', DeviceCreateView.as_view(), name='create-device'),
)
