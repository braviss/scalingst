from django.contrib import admin
from publication.models import Article, Category



@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ["title", "created_at", "slug", "author"]
    list_filter = ('status', 'created_at')
    ordering = ["-created_at"]
    exclude = ["last_modify_time"]
    prepopulated_fields = {'slug': ('title',)}
    fields = ('title',
              'slug',
              'body',
              'category',
              'image',
              'status',
              'type',
              'author',
              'created_at')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug",]