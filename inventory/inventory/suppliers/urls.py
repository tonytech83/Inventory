from django.urls import path

from inventory.suppliers.views import SupplierListView, SupplierCreateApiView, SupplierDeleteView, \
    SupplierUpdateApiView

urlpatterns = (
    path('', SupplierListView.as_view(), name='supplier-list'),
    path('create/', SupplierCreateApiView.as_view(), name='create-supplier'),

    path('edit/<int:pk>/', SupplierUpdateApiView.as_view(), name='edit-supplier'),

    path('delete/<int:pk>/', SupplierDeleteView.as_view(), name='delete-supplier'),
)
