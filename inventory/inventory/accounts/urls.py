from django.urls import path, include

from inventory.accounts.views import LoginView, RegisterUser, LogoutView, DetailsProfile

urlpatterns = (
    path('login/', LoginView.as_view(), name='login-user'),
    path('register/', RegisterUser.as_view(), name='register-user'),
    path('logout/', LogoutView.as_view(), name='logout-user'),

    path('details/', DetailsProfile.as_view(), name='details-profile'),

)
