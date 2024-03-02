from django.urls import path

from inventory.business.views import CreateBusinessView, BusinessView

urlpatterns = (
    path('<int:pk>/', BusinessView.as_view(), name='business'),
    path('create/', CreateBusinessView.as_view(), name='create-business'),
)
