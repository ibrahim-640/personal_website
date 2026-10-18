from django import forms
from .models import Inquiry


class InquiryForm(forms.ModelForm):
    message = forms.CharField(max_length=3000, widget=forms.Textarea)
    accepted_terms = forms.BooleanField(
        required=True,
        error_messages={'required': 'Please accept the Terms of Service to continue.'},
    )
    # Trap field: real visitors never see it, so never fill it in
    hp_ref = forms.CharField(required=False)

    class Meta:
        model = Inquiry
        fields = ['name', 'email', 'package', 'message', 'accepted_terms']