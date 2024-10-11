# admin.py

from django.contrib import admin
from .models import Goal, GoalCompletion, Challenge, WhitelistedEmail

# Register the Goal model in the Django admin site to allow CRUD operations via the admin interface
admin.site.register(Goal)

# Register the GoalCompletion model to manage goal completion records via the admin site
admin.site.register(GoalCompletion)

# Register the Challenge model to manage challenges in the admin interface
admin.site.register(Challenge)

# Custom admin configuration for the WhitelistedEmail model
@admin.register(WhitelistedEmail)
class WhitelistedEmailAdmin(admin.ModelAdmin):
    """
    Admin configuration for managing WhitelistedEmail entries.
    """
    # Display email and active status in the admin list view
    list_display = ('email', 'active')

    # Enable filtering by active status
    list_filter = ('active',)

    # Enable searching by email in the admin search bar
    search_fields = ('email',)

    # Order the email entries alphabetically
    ordering = ('email',)
