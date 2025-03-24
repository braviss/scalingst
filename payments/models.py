from django.db import models
from django.conf import settings

class Payment(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("rejected", "Rejected"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name="User"
    )

    payment_details = models.TextField(
        verbose_name="Payment details"
    )
    screenshot = models.ImageField(
        upload_to="payment_proofs/",
        null=True,
        blank=True,
        verbose_name="Payment screenshot"
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="pending",
        verbose_name="Status"
    )
    invite_code = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Invite Code"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created at"
    )
    confirmed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="confirmed_payments",
        verbose_name="Confirmed by"
    )
    confirmed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Confirmed at"
    )

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"

    def __str__(self):
        return f"Payment {self.id} - {self.user.username} - {self.status}"
