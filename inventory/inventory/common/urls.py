from django.urls import path

from inventory.common.views import DashboardView, HomeView

urlpatterns = (
    path('', DashboardView.as_view(), name='dashboard'),
    path('home/', HomeView.as_view(), name='home-page')
)
