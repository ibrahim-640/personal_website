from django.db import models

# Create your models here.
class Project(models.Model):
    CATEGORY_CHOICES = [
        ('Web', 'Web Development'),
        ('Android', 'Android  Development'),
    ]
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True,blank=True)
    short_description =models.CharField(max_length=255,blank=True)
    description = models.TextField()
    technologies = models.CharField(max_length=255,help_text="Technologies used in the project, separated by commas",blank=True)
    image = models.URLField(blank=True)
    project_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Web')
    created_at = models.DateTimeField(auto_now_add=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.title.lower().replace(' ', '-')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
