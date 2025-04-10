from django.contrib.auth import login, logout
from django.contrib.auth.views import (LoginView,
                                       PasswordResetConfirmView as BasePasswordResetConfirmView,
                                       PasswordResetView as BasePasswordResetView)
from django.views import View
from view_breadcrumbs import ListBreadcrumbMixin, BaseBreadcrumbMixin
from django.utils.timezone import now
from offers.models import Offer
from users.models import CustomUser, EmailVerificationCode
from django.urls import reverse_lazy
from users.forms import RegistrationForm, CustomLoginForm, EmailVerificationForm
from django.views.generic import (
    CreateView, TemplateView, FormView, ListView, DeleteView,
)
from django.http import JsonResponse
from django.core.mail import send_mail
from django.contrib import messages
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.auth.mixins import LoginRequiredMixin
from users.forms import ProfileForm
from django.shortcuts import render, redirect, get_object_or_404


class RegistrationView(CreateView):
    model = CustomUser
    form_class = RegistrationForm
    template_name = 'registration.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        send_verification_email(self.object)
        return redirect('accounts:verify_email', user_id=self.object.id)


class CustomLoginView(LoginView):
    template_name = 'login.html'
    form_class = CustomLoginForm

    def form_valid(self, form):
        user = form.get_user()

        if not user.is_email_verified:
            messages.error(self.request, "Пожалуйста, подтвердите ваш email.")
            return redirect('accounts:verify_email', user_id=user.id)

        return super().form_valid(form)

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url and url_has_allowed_host_and_scheme(
                url=next_url,
                allowed_hosts={self.request.get_host()},
                require_https=self.request.is_secure(),
        ):
            return next_url

        return reverse_lazy('home')




class UserAccountView(LoginRequiredMixin, TemplateView, BaseBreadcrumbMixin):
    template_name = 'profile.html'
    crumbs = [("Profile", reverse_lazy('offers:offer_list'))]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.avatar and hasattr(user.avatar, 'url'):
            context['avatar'] = user.avatar.url
        else:
            context['avatar'] = None
        # context['avatar'] = user.avatar.url
        context['username'] = user.username
        context['email'] = user.email
        context['is_premium'] = user.is_premium
        context['premium_since'] = user.premium_since
        context['referred_users'] = user.referred_users()
        return context


class MyOffersListView(LoginRequiredMixin, ListView):
    model = Offer
    template_name = 'proffile_offers_list.html'
    context_object_name = 'offers'
    paginate_by = 10

    def get_queryset(self):
        return Offer.objects.filter(author=self.request.user).order_by('-created_at')



class ReferredUsersView(LoginRequiredMixin, TemplateView):
    template_name = 'referred_users.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context['referred_users'] = user.referred_users()

        return context



class EditProfileView(LoginRequiredMixin, FormView):
    template_name = 'edit_profile.html'
    form_class = ProfileForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('accounts:dashboard', kwargs={'username': self.request.user.username})



def send_verification_email(user):
    code, created = EmailVerificationCode.objects.get_or_create(
        user=user,
        defaults={"code": EmailVerificationCode.generate_code(), "created_at": now()}
    )

    if not created:
        code.code = EmailVerificationCode.generate_code()
        code.created_at = now()
        code.save()

    send_mail(
        "Подтверждение почты",
        f"Ваш код подтверждения: {code.code}",
        "noreply@scalingst.com",
        [user.email],
        fail_silently=False,
    )



class VerifyEmailView(FormView):
    template_name = "verify_email.html"
    form_class = EmailVerificationForm

    def dispatch(self, request, *args, **kwargs):
        self.user = get_object_or_404(CustomUser, id=kwargs['user_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        code = form.cleaned_data['code']
        verification = EmailVerificationCode.objects.filter(user=self.user, code=code).first()

        if verification and not verification.is_expired():
            self.user.is_active = True
            self.user.is_email_verified = True
            self.user.save()
            verification.delete()
            login(self.request, self.user)
            return super().form_valid(form)
        else:
            messages.error(self.request, "Неверный или просроченный код. Новый код был отправлен на ваш email.")
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy("home")


class ResendVerificationCodeView(View):
    def post(self, request, *args, **kwargs):
        try:
            user_id = request.json().get('user_id')
            user = CustomUser.objects.get(id=user_id)
            send_verification_email(user)
            return JsonResponse({"success": True})
        except CustomUser.DoesNotExist:
            return JsonResponse({"success": False, "message": "Пользователь не найден."})




class PasswordResetView(BasePasswordResetView):
    email_template_name = 'password_reset_email.txt'
    html_email_template_name = 'password_reset_email.html'
    template_name = 'password_reset_form.html'
    success_url = reverse_lazy('accounts:password_reset_done')




class PasswordResetConfirmView(BasePasswordResetConfirmView):
    success_url = reverse_lazy('accounts:password_reset_complete')
    template_name = 'password_reset_confirm.html'



class UserDeleteView(DeleteView):
    model = CustomUser
    success_url = reverse_lazy('home')
    template_name = 'user_confirm_delete.html'

    def get_object(self, queryset=None):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        logout(request)
        user.delete()
        return redirect(self.success_url)