import logging
from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render

from .forms import InquiryForm

logger = logging.getLogger(__name__)


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def packages(request):
    return render(request, 'packages.html')


def process(request):
    return render(request, 'process.html')
def privacy(request):
    return render(request, 'privacy.html')


def send_inquiry_email(inquiry):
    """Email the inquiry to you. A failure is logged but never loses the saved inquiry."""
    recipient = getattr(settings, 'CONTACT_EMAIL', settings.EMAIL_HOST_USER)
    body = f"""New quote request from the MUTITECH website.

Name:     {inquiry.name}
Email:    {inquiry.email}
Package:  {inquiry.get_package_display()}

Project details:
{inquiry.message}

Reply directly to this email to respond to the client.
"""
    try:
        EmailMessage(
            subject=f"New MUTITECH inquiry: {inquiry.get_package_display()} from {inquiry.name}",
            body=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[recipient],
            reply_to=[inquiry.email],
        ).send()
    except Exception:
        logger.exception("Could not send inquiry email for inquiry %s", inquiry.pk)


def contact(request):
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save()
            send_inquiry_email(inquiry)
            messages.success(request, "Thanks! Your request was sent. Expect a fixed quote within 24 hours.")
            return redirect('contact')
        return render(request, 'contact.html', {'form': form})

    initial = {'package': request.GET.get('package', 'growth')}
    return render(request, 'contact.html', {'form': InquiryForm(initial=initial)})