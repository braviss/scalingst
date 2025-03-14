from django.contrib import admin
from offers.models import Offer, Category, Complaint
from django.utils import timezone


@admin.action(description="Mark selected stories as published")
def make_published(modeladmin, request, queryset):
    queryset.update(status="pu")



@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ["title", "created_at", "slug", "author"]
    list_filter = ('status', 'created_at', 'is_premium')
    ordering = ["-created_at"]
    exclude = ["last_modify_time"]
    actions = [make_published]
    prepopulated_fields = {'slug': ('title',)}

    fields = ('title',
              'slug',
              'body',
              'category',
              'image',
              'status',
              'author',
              'country',
              'url',
              'is_premium',
              'premium_at',
              'created_at')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug",]
    prepopulated_fields = {'slug': ('name',)}



@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ["offer", "user", "status"]
    list_filter = ('status', 'created_at')
    ordering = ["-created_at"]
    fields = ('offer',
              'user',
              'text',
              'status',
              'admin_comment')