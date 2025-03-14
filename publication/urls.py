from django.urls import path
from publication import views

app_name = "publication"

urlpatterns = [
    path('list/',
         views.ArticleListView.as_view(),
         name='article_list'),


    path('page/<slug:slug>',
         views.ArticleDetailView.as_view(),
         name='article_detail'),
]