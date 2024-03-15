from django.urls import path

from inventory.suppliers.views import SupplierListView, SupplierCreateView, SupplierEditView, SupplierDeleteView

urlpatterns = (
    path('', SupplierListView.as_view(), name='supplier-list'),
    path('create/', SupplierCreateView.as_view(), name='create-supplier'),
    path('edit/<int:pk>/', SupplierEditView.as_view(), name='edit-supplier'),
    path('delete/<int:pk>/', SupplierDeleteView.as_view(), name='delete-supplier'),
)
