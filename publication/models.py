import uuid
from abc import abstractmethod
from django.db import models
from django.urls import reverse
from django.utils import timezone
from tinymce import models as tinymce_models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.conf import settings
from transliterate import translit


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(default=timezone.now)
    last_modify_time = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True




class Article(BaseModel):
    """
    Model for storing article data
    """
    STATUS_ARTICLE_CHOICES = [
        ("pe", "Pending"),
        ("pu", "Published"),
        ("re", "Rejected"),
    ]
    TYPE = (
        ('a', _('Article')),
        ('p', _('Page')),
    )

    title = models.CharField(verbose_name=_('Title'),
                             max_length=100,
                             unique=True)
    body = tinymce_models.HTMLField()
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    category = models.ForeignKey('Category',
                                 on_delete=models.SET_NULL,
                                 null=True, blank=True)
    image = models.ImageField(upload_to='article_img',
                              null=True, blank=True,
                              default='media/default_article.svg')
    status = models.CharField(max_length=2,
                              choices=STATUS_ARTICLE_CHOICES,
                              default='pe')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    type = models.CharField(max_length=1, choices=TYPE, default='a')

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"
        db_table_comment = "Article table braviss"
        get_latest_by = 'created_at'


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(translit(self.title, 'ru', reversed=True))
        super().save(*args, **kwargs)


    def get_absolute_url(self):
        return reverse('publication:article_detail', kwargs={'slug': self.slug})


    def __str__(self):
        return self.title


class Category(BaseModel):
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(max_length=30, blank=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)