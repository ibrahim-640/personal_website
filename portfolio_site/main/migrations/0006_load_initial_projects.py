from django.db import migrations
from django.core.management import call_command
import os

def load_fixture(apps, schema_editor):
    # ONLY load if NO projects exist (fresh database)
    Project = apps.get_model('main', 'Project')
    if Project.objects.count() == 0:
        fixture_path = os.path.join(os.path.dirname(__file__), '../fixtures/projects_fixture.json')
        if os.path.exists(fixture_path):
            call_command('loaddata', 'projects_fixture.json', app_label='main')
            print("✅ Loaded initial projects (fresh database only)")

class Migration(migrations.Migration):
    dependencies = [
        ('main', '0005_alter_project_category_alter_project_image'),
    ]

    operations = [
        migrations.RunPython(load_fixture),
    ]