from django.contrib import admin
from .models import Inquiry

admin.site.site_header = "MUTITECH Admin"
admin.site.site_title = "MUTITECH Admin Portal"
admin.site.index_title = "Inquiries and quotes"


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'package', 'status', 'created_at')
    list_filter = ('status', 'package', 'created_at')
    list_editable = ('status',)
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('created_at',)