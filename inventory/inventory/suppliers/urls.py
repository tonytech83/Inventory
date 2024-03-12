from django.urls import path

from inventory.suppliers.views import SupplierListView, SupplierCreateView, SupplierEditView

urlpatterns = (
    path('', SupplierListView.as_view(), name='supplier-list'),
    path('create-supplier/', SupplierCreateView.as_view(), name='create-supplier'),
    path('edit-supplier/<int:pk>/', SupplierEditView.as_view(), name='edit-supplier'),
)
