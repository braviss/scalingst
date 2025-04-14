from django.contrib import admin
from feedback.models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ["name", "feedback_type"]
    readonly_fields = ('created_at',)
    fields = ('name',
              'email',
              'feedback_type',
              'message',
              'created_at'
              )