# Generated by Django 4.1.5 on 2023-04-13 14:13

from django.db import migrations, models
import django.db.models.deletion
import enumchoicefield.fields
import payment.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("borrowing", "0008_alter_borrowing_expected_return_date"),
    ]

    operations = [
        migrations.CreateModel(
            name="Payment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    enumchoicefield.fields.EnumChoiceField(
                        enum_class=payment.models.StatusEnum, max_length=7
                    ),
                ),
                (
                    "type",
                    enumchoicefield.fields.EnumChoiceField(
                        enum_class=payment.models.TypeEnum, max_length=7
                    ),
                ),
                ("session_url", models.URLField(max_length=255)),
                ("session_id", models.TextField()),
                (
                    "borrowing",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="payment",
                        to="borrowing.borrowing",
                    ),
                ),
            ],
        ),
    ]
