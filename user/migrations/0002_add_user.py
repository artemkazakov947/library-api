from django.contrib.auth.hashers import make_password
from django.db import migrations

from user.models import User


def add_user(apps, schema_editor):
    user = User(
        email="admin@example.com",
        password=make_password("test_admin12345"),
        is_staff=True,
        is_superuser=True,
    )
    user.save()


def remove_user(apps, schema_editor):
    if User.objects.filter(email="admin@example.com").exists():
        User.objects.get(email="admin@example.com").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(add_user, remove_user),
    ]
