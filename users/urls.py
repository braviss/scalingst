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
    path('verify-email/<int:user_id>/', views.VerifyEmailView.as_view(), name='verify_email'),
    path('send-verification-code/', views.ResendVerificationCodeView.as_view(), name='resend_verification_code'),

    path('password_reset/',
         views.PasswordResetView.as_view(),
         name='password_reset'),
    path(
        'password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
        name='password_reset_done',
    ),
    path(
        'reset/<uidb64>/<token>/',
        views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
        name='password_reset_confirm',
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
        name='password_reset_complete',
    ),
    path('delete-account/', views.UserDeleteView.as_view(), name='delete_account'),
]
