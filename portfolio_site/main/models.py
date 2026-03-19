from django.db import models
import cloudinary
import cloudinary.uploader
import cloudinary.api
import os


class Project(models.Model):
    CATEGORY_CHOICES = [
        ('Web', 'Web Development'),
        ('Android', 'Android Development'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    short_description = models.CharField(max_length=255, blank=True)
    description = models.TextField()

    technologies = models.CharField(
        max_length=255,
        help_text="Technologies used in the project, separated by commas",
        blank=True
    )

    image = models.ImageField(upload_to='projects/', blank=True, null=True)

    project_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='Web'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Generate slug if not provided
        if not self.slug:
            self.slug = self.title.lower().replace(' ', '-')

        # PRESERVATION: Keep existing Cloudinary URLs
        if self.pk:  # Existing project
            try:
                old_project = Project.objects.get(pk=self.pk)
                # If image is already a Cloudinary URL (http or https)
                if old_project.image and ('cloudinary.com' in str(old_project.image)):
                    # If image field hasn't changed or is empty
                    if not self.image or str(self.image) == str(old_project.image):
                        self.image = old_project.image
                        print(f"🔄 Preserved Cloudinary URL: {self.image}")
                        super().save(*args, **kwargs)
                        return
            except Project.DoesNotExist:
                pass

        # UPLOAD: Handle new image uploads
        if self.image and hasattr(self.image, 'file'):
            try:
                cloudinary.config(
                    cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME'),
                    api_key=os.environ.get('CLOUDINARY_API_KEY'),
                    api_secret=os.environ.get('CLOUDINARY_API_SECRET'),
                    secure=True
                )

                print(f"📤 Uploading new image to Cloudinary...")
                upload_result = cloudinary.uploader.upload(
                    self.image,
                    folder="projects/",
                    public_id=f"project_{self.slug}_{self.pk or 'new'}",
                    overwrite=True
                )

                self.image = upload_result['url']
                print(f"✅ Image uploaded to Cloudinary: {self.image}")

            except Exception as e:
                print(f"⚠️ Cloudinary upload failed: {e}")

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title