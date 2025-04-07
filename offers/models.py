import uuid
from abc import abstractmethod
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from tinymce import models as tinymce_models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from transliterate import translit
from django_countries.fields import CountryField
from django.urls import reverse
from django.conf import settings

from location.models import Region, Locality


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(default=timezone.now)
    last_modify_time = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True

    @abstractmethod
    def get_absolute_url(self):
        pass


class Offer(BaseModel):
    """
    Model for storing offer data
    """
    STATUS_OFFER_CHOICES = [
        ("pe", "Pending"),
        ("pu", "Published"),
        ("re", "Rejected"),
    ]

    title = models.CharField(verbose_name=_('Title'),
                             max_length=100,
                             unique=True)
    body = tinymce_models.HTMLField()
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    category = models.ForeignKey('Category',
                                 on_delete=models.SET_NULL,
                                 null=True, blank=True)
    region = models.ForeignKey(
        Region,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Область",
        related_name='offers'
    )
    locality = models.ForeignKey(
        Locality,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Населённый пункт",
        related_name='offers'
    )
    image = models.ImageField(upload_to='offer_img',
                              null=True, blank=True,
                              default='media/default_offer.png')
    status = models.CharField(max_length=2,
                              choices=STATUS_OFFER_CHOICES,
                              default='pe')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    country = CountryField(blank_label='Select country', null=True, blank=True)
    url = models.URLField(max_length=200, null=True, blank=True)
    premium_url = models.URLField(max_length=200, null=True, blank=True)

    is_premium = models.BooleanField(default=False)
    premium_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Offer"
        verbose_name_plural = "Offers"
        db_table_comment = "Offer table braviss"
        get_latest_by = 'created_at'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(translit(self.title, 'ru', reversed=True))
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('offers:offer_detail',
                       kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class Category(BaseModel):
    """
    Model for storing offer category data
    """
    name = models.CharField(
        max_length=30,
        unique=True
    )
    slug = models.SlugField(
        max_length=30,
        blank=True
    )
    description = models.TextField(max_length=200)
    image = models.ImageField(
        upload_to='category_img',
        null=True, blank=True
    )

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Complaint(BaseModel):
    """
    Model for user complaints about offers
    """
    STATUS_CHOICES = [
        ("pe", "Pending"),
        ("re", "Reviewed"),
        ("ac", "Accepted"),
        ("de", "Declined"),
    ]

    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name="complaints")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField(verbose_name=_('Complaint text'))
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default="pe")
    admin_comment = models.TextField(blank=True, null=True, verbose_name=_("Admin Comment"))

    class Meta:
        verbose_name = "Complaint"
        verbose_name_plural = "Complaints"
        ordering = ['-created_at']

    def __str__(self):
        return f"Complaint by {self.user} on {self.offer}"
