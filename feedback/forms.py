from django import forms
from .models import Feedback
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox

class FeedbackForm(forms.ModelForm):
    captcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox,
    )
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'feedback_type', 'message']
        widgets = {
            'feedback_type': forms.Select(attrs={'class': 'form-select'}),
            'message': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
