"""
URL configuration for subspace project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from offers.views import HomePageView
from offers.views import external_link_warning
from offers.views import get_cities

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('tinymce/', include('tinymce.urls')),
    path('get_cities/<str:country_code>/', get_cities, name='get_cities'),
]+ static(settings.MEDIA_URL,
           document_root=settings.MEDIA_ROOT)


urlpatterns += i18n_patterns(
    path('account/',
         include(('users.urls', 'accounts'),
                 namespace='accounts')),
    path('offer/',
         include(('offers.urls', 'offers'),
                 namespace='offers')),
    path('notifications/',
         include(('notifications.urls', 'notifications'),
                 namespace='notifications')),

    path('payments/',
         include(('payments.urls', 'payments'),
                 namespace='payments')),

    path('page/',
         include(('publication.urls', 'publication'),
                 namespace='publication')),


    path('i18n/',
         include('django.conf.urls.i18n')),
    path("external-link/",
         external_link_warning,
         name="external_link_warning"),


) + static(settings.MEDIA_URL,
           document_root=settings.MEDIA_ROOT)