from django.contrib import admin
from .models import Region, Locality

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')
    search_fields = ('name',)
    list_filter = ('country',)

@admin.register(Locality)
class LocalityAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'region')
    search_fields = ('name',)
    list_filter = ('type', 'region__country')
