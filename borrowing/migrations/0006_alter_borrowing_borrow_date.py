# Generated by Django 4.1.5 on 2023-01-24 08:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("borrowing", "0005_alter_borrowing_borrow_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="borrowing",
            name="borrow_date",
            field=models.DateField(default=datetime.date(2023, 1, 24)),
        ),
    ]
