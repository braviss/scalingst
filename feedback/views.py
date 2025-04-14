from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from .models import Feedback
from .forms import FeedbackForm

class FeedbackCreateView(CreateView):
    model = Feedback
    form_class = FeedbackForm
    template_name = 'feedback_form.html'
    success_url = reverse_lazy('feedback:thanks')


class FeedbackThanksView(TemplateView):
    template_name = 'feedback_thanks.html'
