from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import CustomUser
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox
from django.contrib.auth.forms import AuthenticationForm

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    captcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox,
    )

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2")


class CustomLoginForm(AuthenticationForm):
    captcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox,
    )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'avatar']


class EmailVerificationForm(forms.Form):
    code = forms.CharField(max_length=6, required=True, label="Введите код")

    def clean_code(self):
        code = self.cleaned_data.get('code')
        if not code:
            raise forms.ValidationError("Пожалуйста, введите код подтверждения.")
        return code