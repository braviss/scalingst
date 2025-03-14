from django.contrib import admin
from notifications.models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ["user", "created_at"]
    fields = ('user',
              'message',
              'is_read'
              )