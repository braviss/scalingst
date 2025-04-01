from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import CustomUser
from .models import Payment
from notifications.models import Notification
from django.conf import settings

@receiver(post_save, sender=Payment)
def create_notification_for_invite(sender, instance, created, **kwargs):
    if not created:

        if instance.status == "confirmed" and instance.invite_code:
            inviter = CustomUser.objects.filter(my_invite_code=instance.invite_code).first()
            if inviter:
                Notification.objects.create(
                    user=inviter,
                    message=f"Под вашим инвайт-кодом зарегистрировался новый пользователь: {instance.user.username}."
                )
