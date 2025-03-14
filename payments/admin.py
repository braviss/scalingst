from django.contrib import admin
from .models import Payment
from django.utils import timezone
from django.contrib.auth import get_user_model

# @admin.register(Payment)
# class PaymentAdmin(admin.ModelAdmin):
#     list_display = ("id", "user", "status", "created_at", "confirmed_by", "confirmed_at")
#     list_filter = ("status", "created_at")
#     search_fields = ("user__username", "confirmed_by__username")
#     readonly_fields = ("created_at", "confirmed_at")
#     actions = ["confirm_payments", "reject_payments"]
#
#     def confirm_payments(self, request, queryset):
#         """Bulk confirm selected payments"""
#         queryset.update(status="confirmed", confirmed_by=request.user)
#     confirm_payments.short_description = "Confirm selected payments"
#
#     def reject_payments(self, request, queryset):
#         """Bulk reject selected payments"""
#         queryset.update(status="rejected")
#     reject_payments.short_description = "Reject selected payments"




@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status", "created_at", "confirmed_by", "confirmed_at")
    list_filter = ("status", "created_at")
    search_fields = ("user__username", "confirmed_by__username")
    readonly_fields = ("created_at", "confirmed_at", "confirmed_by")
    actions = ["confirm_payments", "reject_payments"]

    def confirm_payments(self, request, queryset):
        for payment in queryset:
            if payment.status != "confirmed":
                payment.status = "confirmed"
                payment.confirmed_by = request.user
                payment.confirmed_at = timezone.now()
                payment.save()
    confirm_payments.short_description = "Confirm selected payments"

    def reject_payments(self, request, queryset):
        queryset.update(status="rejected", confirmed_by=None, confirmed_at=None)
    reject_payments.short_description = "Reject selected payments"

    def save_model(self, request, obj, form, change):
        if obj.status == "confirmed" and not obj.confirmed_by:
            obj.confirmed_by = request.user
            obj.confirmed_at = timezone.now()
        super().save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.status == "confirmed":
            return self.readonly_fields + ("status",)
        return self.readonly_fields
