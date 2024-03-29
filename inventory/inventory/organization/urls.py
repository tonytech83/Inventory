from django.urls import path

from inventory.organization.views import CreateOrganizationView, EditOrganizationView

urlpatterns = (
    path('create/', CreateOrganizationView.as_view(), name='create-organization'),
    path('edit/<int:pk>/', EditOrganizationView.as_view(), name='edit-organization'),
)
