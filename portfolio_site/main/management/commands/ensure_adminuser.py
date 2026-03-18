from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os


class Command(BaseCommand):
    help = 'Ensures an admin user exists using environment variables'

    def handle(self, *args, **options):
        User = get_user_model()

        # Get from environment variables
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

        if username and password and email:
            if not User.objects.filter(username=username).exists():
                User.objects.create_superuser(username, email, password)
                self.stdout.write(
                    self.style.SUCCESS(f'Superuser "{username}" created successfully')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Superuser "{username}" already exists')
                )
        else:
            self.stdout.write(
                self.style.ERROR('Superuser not created: Missing required environment variables')
            )