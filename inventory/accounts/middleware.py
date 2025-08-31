from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class FirstLoginRedirectMiddleware(MiddlewareMixin):
    """
    Middleware to handle redirections based on the first login status of users.

    This middleware checks if the logged-in user is accessing the site for the first time:
    - For superusers, it redirects to the organization creation page after setting the first login flag to False.
    - For regular users, it redirects to their profile details page if they are not already on that page, after
      setting the first login flag to False.

    Attributes:
        request: HttpRequest object containing metadata about the request.

    Returns:
        HttpResponseRedirect if redirection is needed, None otherwise.
    """

    def process_request(self, request):
        if not request.user.is_authenticated:
            return

        user_profile = request.user.profile

        # For a superuser's first login, redirect to the organization creation page
        if request.user.is_superuser and user_profile.is_first_login:
            user_profile.is_first_login = False
            user_profile.save(update_fields=["is_first_login"])
            request.session["first_login_checked"] = True

            return redirect(reverse("create-organization"))

        # For other users' first login, redirect to their profile details page
        elif user_profile.is_first_login:
            user_profile.is_first_login = False
            user_profile.save(update_fields=["is_first_login"])
            request.session["first_login_checked"] = True

            if request.path != reverse("details-profile"):
                return redirect(reverse("details-profile"))
