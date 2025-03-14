from django.contrib.auth.views import (LoginView)
from view_breadcrumbs import ListBreadcrumbMixin, BaseBreadcrumbMixin

from offers.models import Offer
from users.models import CustomUser
from django.urls import reverse_lazy
from users.forms import RegistrationForm, CustomLoginForm
from django.views.generic import (
    CreateView, TemplateView, FormView, ListView,
)
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.auth.mixins import LoginRequiredMixin
from users.forms import ProfileForm

class RegistrationView(CreateView):
    model = CustomUser
    form_class = RegistrationForm
    template_name = 'registration.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        return response


class CustomLoginView(LoginView):
    template_name = 'login.html'
    form_class = CustomLoginForm

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

        context['avatar'] = user.avatar.url
        context['username'] = user.username
        context['email'] = user.email
        context['is_premium'] = user.is_premium
        context['premium_since'] = user.premium_since
        return context


class MyOffersListView(LoginRequiredMixin, ListView):
    model = Offer
    template_name = 'proffile_offers_list.html'
    context_object_name = 'offers'
    paginate_by = 10

    def get_queryset(self):
        return Offer.objects.filter(author=self.request.user).order_by('-created_at')




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



