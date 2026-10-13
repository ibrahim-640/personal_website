from django.db import migrations


def load_fixture(apps, schema_editor):
    # Intentionally empty: the Project model and its fixture were removed
    # in the MUTITECH conversion. The file is kept so the migration history stays intact.
    return


class Migration(migrations.Migration):
    dependencies = [
        ('main', '0005_alter_project_category_alter_project_image'),
    ]

    operations = [
        migrations.RunPython(load_fixture, migrations.RunPython.noop),
    ]