from django.urls import path
from users import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('profile/<str:username>/',
         views.UserAccountView.as_view(),
         name='dashboard'),
    path('signup/',
         views.RegistrationView.as_view(),
         name='signup'),
    path('signin/',
         views.CustomLoginView.as_view(),
         name='signin'),
    path('logout/',
         auth_views.LogoutView.as_view(),
         name='logout'),
    path('edit/',
         views.EditProfileView.as_view(),
         name='edit_profile'),
    path('offers/', views.MyOffersListView.as_view(), name='my_offers'),
]
