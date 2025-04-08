from django import forms
from offers.models import Offer, Complaint
from cities_light.models import City, Country
from tinymce.widgets import TinyMCE


class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ('title', 'body', 'image', 'category', 'country', 'region', 'url', 'premium_url')
        widgets = {'body': TinyMCE(attrs={'cols': 80, 'rows': 30})}



class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ["text"]
        widgets = {'text': TinyMCE(attrs={'cols': 80, 'rows': 30})}