from django import template
from django.utils.timezone import now
from datetime import timedelta

register = template.Library()

@register.filter
def display_registered_time(value):
    if not value:
        return ""
    
    time_difference = now() - value

    if time_difference < timedelta(minutes=1):
        return "just now"
    elif time_difference < timedelta(hours=1):
        minutes = int(time_difference.total_seconds() // 60)
        return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
    elif time_difference < timedelta(days=1):
        hours = int(time_difference.total_seconds() // 3600)
        return f"{hours} hour{'s' if hours > 1 else ''} ago"
    else:
        # Only display the date after 24 hours
        return value.strftime("%d/%m/%Y")  # Example: 08/01/2025
