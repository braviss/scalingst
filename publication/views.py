from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from publication.models import Article
from view_breadcrumbs import ListBreadcrumbMixin, DetailBreadcrumbMixin


class ArticleListView(ListBreadcrumbMixin, ListView):
    model = Article
    template_name = 'publication_list.html'
    context_object_name = 'articles'
    ordering = '-created_at'
    paginate_by = 10

    def get_queryset(self):
        return Article.objects.filter(status='pu', type='a').order_by('-created_at')


class ArticleDetailView(DetailBreadcrumbMixin, DetailView):
    model = Article
    breadcrumb_use_pk = False
    template_name = 'publication_detail.html'
    count_hit = True
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return Article.objects.filter(status='pu')

    def get_object(self, queryset=None):
        obj = super().get_object()
        self.object = obj
        return obj
