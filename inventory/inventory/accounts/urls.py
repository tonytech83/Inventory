from django.urls import path

from inventory.accounts.views import LoginView, RegisterUserView, DetailsProfileView, EditProfileView, \
    PasswordChangeView, PasswordChangeDoneView, logout_user

urlpatterns = (
    path('login/', LoginView.as_view(), name='login-user'),
    path('register/', RegisterUserView.as_view(), name='register-user'),
    path('logout/', logout_user, name='logout-user'),
    path('edit/<int:pk>/', EditProfileView.as_view(), name='edit-profile'),

    path('details/', DetailsProfileView.as_view(), name='details-profile'),
    path('password_change/', PasswordChangeView.as_view(), name='password-change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
)
