from django.urls import path

from inventory.business.views import CreateBusinessView

urlpatterns = (
    path('create/', CreateBusinessView.as_view(), name='create-business'),
)
