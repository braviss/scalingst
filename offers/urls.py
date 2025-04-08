from django.urls import path
from offers import views


urlpatterns = [
    path('list',
         views.OfferListView.as_view(),
         name='offer_list'),
    path('<slug:slug>',
         views.OfferDetailView.as_view(),
         name='offer_detail'),
    path('create/',
         views.OfferCreateView.as_view(),
         name='offer_create'),
    path('update/<slug:slug>/',
         views.OfferUpdateView.as_view(),
         name='offer_update'),
    path('delete/<slug:slug>',
         views.OfferDeleteView.as_view(),
         name='offer_delete'),

    path('users/<str:username>/',
         views.UserOfferListView.as_view(),
         name='user_offers'),

    path("<slug:slug>/complaint/",
         views.ComplaintCreateView.as_view(),
         name="offer_complaint"),

    path('category/',
         views.CategoryListView.as_view(),
         name='category_list'),

]
