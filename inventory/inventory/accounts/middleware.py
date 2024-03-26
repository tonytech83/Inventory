from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class FirstLoginRedirectMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Skip middleware for unauthenticated users or if the check has already been done
        if not request.user.is_authenticated or request.session.get('first_login_checked', False):
            return

        # Mark that the first login check has been done to avoid repeated checks
        request.session['first_login_checked'] = True

        # If it's a GET request to the login URL, and the user is already authenticated,
        # it indicates a redirect after the first successful login
        if request.path == reverse('login-user') and request.method == 'GET':
            if request.user.profile.is_first_login:


                return redirect(reverse('details-profile'))

