from django.urls import path
from . import views

urlpatterns = [
    path('get_regions/<str:country_code>/', views.get_regions, name='get_regions'),
    path('get_localities/<str:region_code>/', views.get_localities, name='get_localities'),

]
