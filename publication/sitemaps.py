from django.contrib.sitemaps import Sitemap
from publication.models import Article


class ArticleSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9
    protocol = 'https'
    i18n = True
    languages = ['uk', 'en', 'ru']


    def items(self):
        return Article.objects.all()

    def lastmod(self, obj):
        return obj.created_at

    def location(self, obj):
        return obj.get_absolute_url()
