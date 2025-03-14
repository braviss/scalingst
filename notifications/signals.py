from django.db.models.signals import post_save
from django.dispatch import receiver
from offers.models import Offer, Complaint
from notifications.models import Notification

@receiver(post_save, sender=Offer)
def notify_user_on_status_change(sender, instance, created, **kwargs):
    if not created and instance.status == "pu":
        Notification.objects.create(
            user=instance.author,
            message=f"Ваша публикация '{instance.title}' была опубликована!"
        )



@receiver(post_save, sender=Complaint)
def notify_user_on_status_change(sender, instance, created, **kwargs):
    if not created and instance.status == "ac":
        Notification.objects.create(
            user=instance.user,
            message=f"Ваша жалоба обработана. Ответ администратора: {instance.admin_comment}."
        )
