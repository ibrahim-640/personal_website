from django.db import migrations
from django.core.management import call_command
import os

def load_fixture(apps, schema_editor):
    # Check if we're on Render (optional, but safe)
    if 'RENDER' in os.environ:
        Project = apps.get_model('main', 'Project')
        if Project.objects.count() == 0:
            fixture_path = os.path.join(os.path.dirname(__file__), '../fixtures/projects_fixture.json')
            if os.path.exists(fixture_path):
                call_command('loaddata', 'projects_fixture.json', app_label='main')
                print("✅ Projects loaded successfully!")
            else:
                print("⚠️  Fixture file not found")

class Migration(migrations.Migration):
    dependencies = [
        ('main', '0005_alter_project_category_alter_project_image'),
    ]

    operations = [
        migrations.RunPython(load_fixture),
    ]
