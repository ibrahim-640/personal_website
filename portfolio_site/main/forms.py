from django import forms
from .models import Inquiry


class InquiryForm(forms.ModelForm):
    accepted_terms = forms.BooleanField(
        required=True,
        error_messages={'required': 'Please accept the Terms of Service to continue.'},
    )

    class Meta:
        model = Inquiry
        fields = ['name', 'email', 'package', 'message', 'accepted_terms']