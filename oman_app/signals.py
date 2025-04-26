from allauth.socialaccount.signals import social_account_added, social_account_updated
from django.dispatch import receiver
from django.contrib.auth import get_user_model
import requests
from django.core.files.base import ContentFile

User = get_user_model()

@receiver(social_account_added)
@receiver(social_account_updated)
def save_google_profile_picture(request, sociallogin, **kwargs):
    """
    When a user logs in with Google, save their profile image.
    """
    if sociallogin.account.provider == 'google':
        user = sociallogin.user
        extra_data = sociallogin.account.extra_data  # Fetch Google profile data
        
        # Get profile image URL from Google
        google_profile_image = extra_data.get('picture')

        if google_profile_image:
            # Download the image from Google
            response = requests.get(google_profile_image)
            if response.status_code == 200:
                # Save image to user model (assuming user has an 'image' field)
                user.image.save(f"{user.username}_google.jpg", ContentFile(response.content), save=True)
