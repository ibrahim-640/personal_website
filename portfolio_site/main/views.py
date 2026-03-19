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


from django.http import HttpResponse
import re
import cloudinary.uploader
from django.core.files.base import ContentFile
import requests
from io import BytesIO


def force_fix_images(request):
    output = []
    fixed_count = 0
    error_count = 0

    # Get ALL projects
    projects = Project.objects.all()
    output.append(f"Found {projects.count()} projects")

    for project in projects:
        output.append(f"\n--- Processing: {project.title} ---")

        # Check if image exists and is malformed
        if project.image:
            old_url = str(project.image)
            output.append(f"Current URL: {old_url[:100]}...")

            # Extract clean Cloudinary URL if it exists in the mess
            if 'res.cloudinary.com' in old_url:
                # Extract just the Cloudinary part
                match = re.search(r'(https?://res\.cloudinary\.com[^\s]+)', old_url)
                if match:
                    clean_url = match.group(1)
                    output.append(f"Found Cloudinary URL: {clean_url}")

                    # Test if the URL is actually accessible
                    try:
                        response = requests.head(clean_url, timeout=5)
                        if response.status_code == 200:
                            # URL works! Just save it
                            project.image = clean_url
                            project.save()
                            output.append(f"✅ Saved clean URL")
                            fixed_count += 1
                        else:
                            output.append(f"⚠️ URL returns {response.status_code}")
                            # URL doesn't work, need to re-upload
                            error_count += 1
                    except:
                        output.append(f"⚠️ URL not accessible")
                        error_count += 1
                else:
                    output.append(f"❌ Could not extract Cloudinary URL")
                    error_count += 1
            else:
                output.append(f"ℹ️ Not a Cloudinary URL - may need manual upload")
        else:
            output.append(f"ℹ️ No image")

    output.append(f"\n=== SUMMARY ===")
    output.append(f"✅ Fixed: {fixed_count}")
    output.append(f"❌ Need manual re-upload: {error_count}")

    return HttpResponse("<br>".join(output).replace("\n", "<br>"))