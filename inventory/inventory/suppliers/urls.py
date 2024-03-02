from django.urls import path

from inventory.suppliers.views import SupplierListView, SupplierCreateView

urlpatterns = (
    path('', SupplierListView.as_view(), name='supplier-list'),
    path('create-supplier/', SupplierCreateView.as_view(), name='create-supplier'),
)
