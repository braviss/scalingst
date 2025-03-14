from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser
from offers.models import Offer
from django.utils.timezone import now

@receiver(post_save, sender=CustomUser)
def update_user_offers(sender, instance, **kwargs):
    """
    Если пользователь становится премиум, обновляем все его офферы
    """
    if instance.is_premium:
        Offer.objects.filter(author=instance).update(
            is_premium=True,
            premium_at=now()
        )
    else:
        Offer.objects.filter(author=instance).update(
            is_premium=False,
            premium_at=None
        )
