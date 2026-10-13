from django.db import models


class Inquiry(models.Model):
    PACKAGE_CHOICES = [
        ('starter', 'Starter · KES 15K'),
        ('growth', 'Growth · KES 30K'),
        ('pro', 'Pro · KES 50K'),
        ('unsure', 'Not sure yet'),
    ]
    STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('quoted', 'Quoted'),
        ('won', 'Won'),
        ('closed', 'Closed'),
    ]

    name = models.CharField(max_length=120)
    email = models.EmailField()
    package = models.CharField(max_length=20, choices=PACKAGE_CHOICES, default='growth')
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Inquiries'

    def __str__(self):
        return f"{self.name} · {self.get_package_display()}"