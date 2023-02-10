from django.contrib.auth import get_user_model
from django.db import migrations


def create_superuser(user, schema_editor):
    superuser = get_user_model().objects.create_superuser(
        "admin@example.com", "test_admin12345"
    )
    superuser.save()


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]
