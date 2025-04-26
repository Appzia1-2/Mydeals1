from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth import get_user_model

User = get_user_model()

class MyAccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        """ Prevents email-based signup if using Google. """
        return True  # Keep this as True if you want normal signups

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        """Link social account to an existing user with the same email."""
        email = sociallogin.account.extra_data.get('email')

        if not email:
            return  # No email, let Allauth handle it

        try:
            # Check if a user with the same email already exists
            user = User.objects.get(email=email)

            # If the user exists but is not linked to this social account, link them
            sociallogin.connect(request, user)

        except User.DoesNotExist:
            pass  # Continue with normal signup flow
