from django.urls import path, include

from inventory.accounts.views import LoginView, RegisterUserView, LogoutView, DetailsProfileView, EditProfileView, \
    PasswordChangeView, PasswordChangeDoneView

urlpatterns = (
    path('login/', LoginView.as_view(), name='login-user'),
    path('register/', RegisterUserView.as_view(), name='register-user'),
    path('logout/', LogoutView.as_view(), name='logout-user'),

    path('details/', DetailsProfileView.as_view(), name='details-profile'),
    path('password_change/', PasswordChangeView.as_view(), name='password-change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('eidt/<int:pk>/', EditProfileView.as_view(), name='edit-profile'),
)
