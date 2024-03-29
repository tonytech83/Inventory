from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class FirstLoginRedirectMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Skip middleware for unauthenticated users
        if not request.user.is_authenticated:
            return

        # Skip if first login check has been done
        if request.session.get('first_login_checked', False):
            return

        user_profile = request.user.profile
        # print(user_profile)
        # print(user_profile.is_first_login)

        # For a superuser's first login, redirect to the organization creation page
        if request.user.is_superuser and user_profile.is_first_login:
            user_profile.is_first_login = False
            user_profile.save(update_fields=['is_first_login'])
            request.session['first_login_checked'] = True

            return redirect(reverse('create-organization'))

        # For other users' first login, redirect to their profile details page
        elif user_profile.is_first_login:
            user_profile.is_first_login = False
            user_profile.save(update_fields=['is_first_login'])
            request.session['first_login_checked'] = True

            if request.path != reverse('details-profile'):
                return redirect(reverse('details-profile'))
