from django.urls import path

from inventory.suppliers.views import SupplierListView, SupplierCreateView, SupplierDeleteView, \
    SupplierUpdateView

urlpatterns = (
    path('', SupplierListView.as_view(), name='supplier-list'),
    path('create/', SupplierCreateView.as_view(), name='create-supplier'),

    path('edit/<int:pk>/', SupplierUpdateView.as_view(), name='edit-supplier'),

    path('delete/<int:pk>/', SupplierDeleteView.as_view(), name='delete-supplier'),
)
