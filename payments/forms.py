from django import forms
from .models import Payment

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ["payment_details", "screenshot"]
        widgets = {
            "payment_details": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Enter payment details..."}),
            "screenshot": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }
