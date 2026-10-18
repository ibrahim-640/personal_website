import logging
from django.conf import settings
from django.core.cache import cache
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

from django.conf import settings
from django.http import HttpResponse
from django.urls import reverse

def robots(request):
    lines = [
        'User-agent: *',
        'Allow: /',
        f'Sitemap: {settings.SITE_URL}/sitemap.xml',
    ]
    return HttpResponse('\n'.join(lines) + '\n', content_type='text/plain')


def sitemap(request):
    names = ['home', 'about', 'packages', 'process', 'contact', 'privacy']
    entries = ''.join(
        f'<url><loc>{settings.SITE_URL}{reverse(name)}</loc></url>' for name in names
    )
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        f'{entries}</urlset>'
    )
    return HttpResponse(xml, content_type='application/xml')


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


def too_many_requests(request, limit=5, window=3600):
    """True when one connection has sent more than `limit` requests within `window` seconds."""
    ip = request.META.get('REMOTE_ADDR', 'unknown')
    key = f'inquiry-rate:{ip}'
    cache.add(key, 0, window)
    return cache.incr(key) > limit


def contact(request):
    if request.method == 'POST':
        if too_many_requests(request):
            messages.error(
                request,
                'Too many requests from this connection. Please wait a while, or reach us on WhatsApp.',
            )
            return render(request, 'contact.html', {'form': InquiryForm(request.POST)}, status=429)

        form = InquiryForm(request.POST)
        if form.is_valid():
            if form.cleaned_data.get('hp_ref'):
                # A bot filled the trap field: pretend it worked, save nothing
                messages.success(request, "Thanks! Your request was sent. Expect a fixed quote within 24 hours.")
                return redirect('contact')
            inquiry = form.save()
            send_inquiry_email(inquiry)
            messages.success(request, "Thanks! Your request was sent. Expect a fixed quote within 24 hours.")
            return redirect('contact')
        return render(request, 'contact.html', {'form': form})

    initial = {'package': request.GET.get('package', 'growth')}
    return render(request, 'contact.html', {'form': InquiryForm(initial=initial)})