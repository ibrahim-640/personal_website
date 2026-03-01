from django.contrib import admin
from django.utils.html import format_html

from .models import Project

# Register your models here.
admin.site.site_header = "Portfolio Admin"
admin.site.site_title = "Portfolio Admin Portal"
admin.site.index_title = "Welcome to Portfolio Admin Dashboard"
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created_at', 'project_url', 'github_url', 'technologies', 'category')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title','category')
    list_filter = ('created_at','technologies','category')
    ordering = ('-created_at',)
    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" />'.format(obj.image.url))
        return "No Image"
    image_tag.short_description = "Preview"
