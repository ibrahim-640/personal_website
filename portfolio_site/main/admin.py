from django.contrib import admin
from django.utils.html import format_html
from .models import Project

admin.site.site_header = "Portfolio Admin"
admin.site.site_title = "Portfolio Admin Portal"
admin.site.index_title = "Welcome to Portfolio Admin Dashboard"


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'category', 'created_at', 'image_preview')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'category', 'technologies')
    list_filter = ('category', 'created_at', 'technologies')
    ordering = ('-created_at',)

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'short_description', 'description', 'category')
        }),
        ('Technologies', {
            'fields': ('technologies',),
            'description': 'Enter technologies separated by commas (e.g., Python, Django, React)'
        }),
        ('Media', {
            'fields': ('image',),
            'description': 'Upload project screenshot or logo'
        }),
        ('Links', {
            'fields': ('project_url', 'github_url'),
            'description': 'Add project links (optional)'
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            # Fix: Handle both string URLs and ImageField objects
            if hasattr(obj.image, 'url'):
                image_url = obj.image.url
            else:
                image_url = obj.image
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 5px;" />',
                image_url
            )
        return "No Image"

    image_preview.short_description = 'Preview'