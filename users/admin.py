from django.contrib import admin
from users.models import CustomUser

# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = [
        "username",
        "first_name",
        "last_name",
        "email",
        "is_email_verified",
        "my_invite_code",
    ]
    list_filter = ["is_email_verified", "is_staff", "is_superuser", "date_joined"]
    search_fields = ["username", "first_name", "last_name", "email", "my_invite_code"]
