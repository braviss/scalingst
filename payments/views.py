from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from view_breadcrumbs import ListBreadcrumbMixin

from offers.mixins import CustomLoginRequiredMixin
from .models import Payment
from .forms import PaymentForm

class PaymentCreateView(LoginRequiredMixin, CreateView):
    model = Payment
    form_class = PaymentForm
    template_name = "payment_form.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)



class PaymentListView(CustomLoginRequiredMixin,
                      ListView):
    model = Payment
    template_name = 'payment_list.html'
    context_object_name = 'payments'
    ordering = '-created_at'
    paginate_by = 8

    def get_queryset(self):
        return Payment.objects.filter(
            user=self.request.user
        ).order_by('created_at')