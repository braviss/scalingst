from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.http import urlencode


# class CustomLoginRequiredMixin(LoginRequiredMixin):
#     def handle_no_permission(self):
#         messages.warning(self.request, "Для доступа к этой странице необходимо авторизоваться.")
#         return redirect('rest_framework:login')


class CustomLoginRequiredMixin(LoginRequiredMixin):
    def handle_no_permission(self):
        login_url = reverse_lazy('accounts:signin')
        next_url = self.request.get_full_path()
        return redirect(f"{login_url}?{urlencode({'next': next_url})}")