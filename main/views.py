from django.shortcuts import render, get_object_or_404
from django.core.mail import EmailMessage
from django.conf import settings
from .models import Project

# Create your views here.
def home(request):
    return render(request, 'home.html',)
def skills(request):
    return render(request,'skills.html')
def services(request):
    return render(request,'services.html')
def projects(request):
    projects = Project.objects.all().order_by('-created_at')
    return render(request,'projects.html',{'projects':projects})
def project_detail(request,slug):
    project = get_object_or_404(Project,slug=slug)
    return render(request,'project_detail.html', {'project':project})
def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == 'POST':
        recipient = getattr(settings, 'CONTACT_EMAIL', settings.EMAIL_HOST_USER)

        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        subject = f"New Service Inquiry from {name}"

        body = f"""
You have received a new message from your portfolio website.

-----------------------------
CLIENT DETAILS
-----------------------------
Full Name: {name}
Email Address: {email}

-----------------------------
MESSAGE
-----------------------------
{message}

-----------------------------
Reply directly to this email to respond to the client.
"""

        email_message = EmailMessage(
            subject=subject,
            body=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[recipient],
            reply_to=[email],  # 🔥 This makes reply go to client
        )

        email_message.send()

        return render(request, 'contact.html', {'success': True})

    return render(request, 'contact.html')
