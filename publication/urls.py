# В publication/urls.py
from django.urls import path
from publication import views

app_name = "publication"

urlpatterns = [
    path('blog/', views.ArticleListView.as_view(), name='article_list'),
    path('<slug:slug>/', views.ArticleDetailView.as_view(), name='article_detail'),
]
